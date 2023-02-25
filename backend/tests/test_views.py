from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Bike, Customer, Sale
from freezegun import freeze_time


class SalesTestCase(APITestCase):
    def test_create_sale(self):
        bike_1 = Bike.objects.create(
            name="Trek Marlin", model="Trek Marlin 6", price=1049.99, units_available=2)
        bike_2 = Bike.objects.create(
            name="Giant Talon", model="Giant Talon 3", price=764.99, units_available=2)
        payload = {
            "bikes": [
                {
                    "id": bike_1.id,
                    "unitsSold": 1
                },
                {
                    "id": bike_2.id,
                    "unitsSold": 1
                }
            ],
            "customer": {
                "email": "bisping@gmail.com",
                "firstName": "Michael",
                "lastName": "Bisping"
            },
            "paymentMethod": "credit/debit",
            "date": "2023-02-19",
            "discountPercentage": 0
        }
        url = "/api/sales/"
        response = self.client.post(url, data=payload, format="json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        # test the api response
        self.assertTrue("id" in response.data)
        self.assertEqual(str(bike_1.price + bike_2.price),
                         str(response.data["net_sale"]))
        self.assertEqual("2023-02-19", response.data["sold_at"])
        self.assertEqual(2, len(response.data["bikes"]))
        for expected_bike_sale_key in ["bike", "units_sold", "units_refunded", "price"]:
            self.assertTrue(
                expected_bike_sale_key in response.data["bikes"][0])
        self.assertEqual("bisping@gmail.com",
                         response.data["customer"]["email"])

        # test the model data
        bike_1.refresh_from_db()
        bike_2.refresh_from_db()
        self.assertEqual(1, bike_1.units_available)
        self.assertEqual(1, bike_2.units_available)

    def test_create_sale_with_insufficient_stock(self):
        bike = Bike.objects.create(
            name="Trek Marlin", model="Trek Marlin 6", price=1049.99, units_available=2)
        payload = {
            "bikes": [
                {
                    "id": bike.id,
                    "unitsSold": 3
                }
            ],
            "customer": {
                "email": "bisping@gmail.com",
                "firstName": "Michael",
                "lastName": "Bisping"
            },
            "paymentMethod": "credit/debit",
            "date": "2023-02-19",
            "discountPercentage": 0
        }
        url = "/api/sales/"
        response = self.client.post(url, data=payload, format="json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        expected_error_message = "3 units are not available for Trek Marlin - Trek Marlin 6. "\
            "Please ensure that bikes have enough stock before making a sale."
        self.assertEqual("SaleCreationError",
                         response.data["error"][0]["type"])
        self.assertEqual(expected_error_message,
                         response.data["error"][0]["message"])

    def test_create_sale_with_discount(self):
        bike_1 = Bike.objects.create(
            name="Trek Marlin", model="Trek Marlin 6", price=1049.99, units_available=2)
        bike_2 = Bike.objects.create(
            name="Giant Talon", model="Giant Talon 3", price=764.99, units_available=2)
        payload = {
            "bikes": [
                {
                    "id": bike_1.id,
                    "unitsSold": 1
                },
                {
                    "id": bike_2.id,
                    "unitsSold": 1
                }
            ],
            "customer": {
                "email": "bisping@gmail.com",
                "firstName": "Michael",
                "lastName": "Bisping"
            },
            "paymentMethod": "credit/debit",
            "date": "2023-02-19",
            "discountPercentage": 10
        }
        url = "/api/sales/"
        response = self.client.post(url, data=payload, format="json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        expected_net_sale = round(bike_1.price + bike_2.price -
                                  (bike_1.price + bike_2.price) * 0.10, 2)
        self.assertEqual(str(expected_net_sale),
                         str(response.data["net_sale"]))

    def test_update_discount(self):
        customer = Customer.objects.create(
            first_name="Michael", last_name="Bisping", email="bisping@gmail.com")
        bike = Bike.objects.create(
            name="Trek Marlin", model="Trek Marlin 6", price=1049.99, units_available=2)
        sale = self.create_sale(customer, bike, discount_percentage=10)

        payload = {
            "discountPercentage": 15
        }
        url = f"/api/sales/{sale.id}/"
        response = self.client.patch(url, data=payload, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected_net_sale = round(1049.99 - 0.15 * 1049.99, 2)
        self.assertEqual(str(expected_net_sale),
                         str(response.data["net_sale"]))
        self.assertEqual(15, response.data["discount_percentage"])

    def test_update_refund_bikes(self):
        customer = Customer.objects.create(
            first_name="Michael", last_name="Bisping", email="bisping@gmail.com")
        bike = Bike.objects.create(
            name="Trek Marlin", model="Trek Marlin 6", price=1049.99, units_available=2)
        sale = self.create_sale(customer, bike, units_sold=1)
        bike.refresh_from_db()
        self.assertEqual(1, bike.units_available)

        payload = {
            "refund": [
                {
                    "id": bike.id,
                    "unitsRefunded": 1
                }
            ]
        }
        url = f"/api/sales/{sale.id}/"
        response = self.client.patch(url, data=payload, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("0.00", response.data["total_sale"])
        self.assertEqual(1, response.data["bikes"][0]["units_refunded"])
        bike.refresh_from_db()
        self.assertEqual(2, bike.units_available)

    def test_update_refund_error_due_to_refunds_exceeding_units_sold(self):
        customer = Customer.objects.create(
            first_name="Michael", last_name="Bisping", email="bisping@gmail.com")
        bike = Bike.objects.create(
            name="Trek Marlin", model="Trek Marlin 6", price=1049.99, units_available=2)
        sale = self.create_sale(customer, bike, units_sold=1)

        payload = {
            "refund": [
                {
                    "id": bike.id,
                    "unitsRefunded": 2
                }
            ]
        }
        url = f"/api/sales/{sale.id}/"
        response = self.client.patch(url, data=payload, format="json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        expected_error_message = "Units refunded for Trek Marlin - Trek Marlin 6 exceed units that were originally sold."
        self.assertEqual("RefundError", response.data["error"][0]["type"])
        self.assertEqual(expected_error_message,
                         response.data["error"][0]["message"])

    def test_update_refund_error_due_to_reducing_units_refunded(self):
        customer = Customer.objects.create(
            first_name="Michael", last_name="Bisping", email="bisping@gmail.com")
        bike = Bike.objects.create(
            name="Trek Marlin", model="Trek Marlin 6", price=1049.99, units_available=2)
        sale = self.create_sale(customer, bike, units_sold=2)

        payload = {
            "refund": [
                {
                    "id": bike.id,
                    "unitsRefunded": 2
                }
            ]
        }
        url = f"/api/sales/{sale.id}/"
        self.client.patch(url, data=payload, format="json")

        payload = {
            "refund": [
                {
                    "id": bike.id,
                    "unitsRefunded": 1
                }
            ]
        }
        url = f"/api/sales/{sale.id}/"
        response = self.client.patch(url, data=payload, format="json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        expected_error_message = "You are attempting to decrease the total units refunded for Trek Marlin - Trek Marlin 6."\
            " This is not allowed."
        self.assertEqual("RefundError", response.data["error"][0]["type"])
        self.assertEqual(expected_error_message,
                         response.data["error"][0]["message"])

    def test_destroy_updates_bike_inventory(self):
        customer = Customer.objects.create(
            first_name="Michael", last_name="Bisping", email="bisping@gmail.com")
        bike = Bike.objects.create(
            name="Trek Marlin", model="Trek Marlin 6", price=1049.99, units_available=2)
        sale = self.create_sale(customer, bike, units_sold=2)
        bike.refresh_from_db()
        self.assertEqual(0, bike.units_available)
        self.assertEqual(1, Sale.objects.count())

        url = f"/api/sales/{sale.id}/"
        response = self.client.delete(url, format="json")
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        bike.refresh_from_db()
        self.assertEqual(2, bike.units_available)
        self.assertEqual(0, Sale.objects.count())

    def create_sale(self, customer, bike, units_sold=1, discount_percentage=0):
        payload = {
            "bikes": [
                {
                    "id": bike.id,
                    "unitsSold": units_sold
                },
            ],
            "customer": {
                "email": customer.email,
                "firstName": customer.first_name,
                "lastName": customer.last_name
            },
            "paymentMethod": "credit/debit",
            "date": "2023-02-19",
            "discountPercentage": discount_percentage
        }
        url = "/api/sales/"
        response = self.client.post(url, data=payload, format="json")
        sale = Sale.objects.get(pk=response.data["id"])
        return sale


class AnalyticsTestCase(APITestCase):
    def test_top_selling_bikes(self):
        bike_1 = Bike.objects.create(
            name="Trek Marlin", model="Trek Marlin 6", price=1100, units_available=2)
        bike_2 = Bike.objects.create(
            name="Giant Talon", model="Giant Talon 3", price=500, units_available=3)
        bike_3 = Bike.objects.create(
            name="Trek Verve", model="Trek Verve 2", price=400, units_available=2)
        customer = Customer.objects.create(
            first_name="Michael", last_name="Bisping", email="bisping@gmail.com")

        self.create_sale(customer, bike_1)
        self.create_sale(customer, bike_2)
        self.create_sale(customer, bike_2)
        self.create_sale(customer, bike_2)
        self.create_sale(customer, bike_3)
        self.create_sale(customer, bike_3)

        response = self.client.get(
            "/api/analytics/topSellingBikes/", format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, len(response.data))
        self.assertEqual(bike_2.id, response.data[0]["bike"]["id"])
        self.assertEqual(bike_1.id, response.data[1]["bike"]["id"])
        self.assertEqual(bike_3.id, response.data[2]["bike"]["id"])

        # expect rounded down percentages
        self.assertEqual(1500, response.data[0]["sales"])
        self.assertEqual(44, response.data[0]["percentage_total_sales"])
        self.assertEqual(800, response.data[2]["sales"])
        self.assertEqual(23, response.data[2]["percentage_total_sales"])

    def test_all_time_sales(self):
        bike_1 = Bike.objects.create(
            name="Trek Marlin", model="Trek Marlin 6", price=1100, units_available=2)
        bike_2 = Bike.objects.create(
            name="Giant Talon", model="Giant Talon 3", price=500, units_available=3)
        customer = Customer.objects.create(
            first_name="Michael", last_name="Bisping", email="bisping@gmail.com")
        self.create_sale(customer, bike_1, units_sold=2,
                         discount_percentage=10)
        sale_2 = self.create_sale(customer, bike_2, units_sold=3)

        # issue some refunds
        payload = {
            "refund": [
                {
                    "id": bike_2.id,
                    "unitsRefunded": 2
                }
            ]
        }
        url = f"/api/sales/{sale_2.id}/"
        response = self.client.patch(url, data=payload, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        response = self.client.get(
            "/api/analytics/allTimeSales/", format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2700, response.data["total_sales"])
        self.assertEqual(220, response.data["total_discount"])
        self.assertEqual(5, response.data["bikes_sold"])
        self.assertEqual(2, response.data["bikes_refunded"])

    @freeze_time("2023-02-24")
    def test_sales_trend(self):
        bike_1 = Bike.objects.create(
            name="Trek Marlin", model="Trek Marlin 6", price=1100, units_available=100)
        customer = Customer.objects.create(
            first_name="Michael", last_name="Bisping", email="bisping@gmail.com")
        sale_dates = ["2022-02-14", "2022-02-24", "2022-03-05", "2022-03-17", "2022-04-04", "2022-04-15", "2022-04-19",
                      "2022-05-04", "2022-05-06", "2022-05-20", "2022-05-29"]
        for date in sale_dates:
            self.create_sale(customer, bike_1, date=date)

        response = self.client.get("/api/analytics/salesTrend/", format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected_data = [
            {
                "year": 2023,
                "month": 2,
                "sales": 0
            },
            {
                "year": 2023,
                "month": 1,
                "sales": 0
            },
            {
                "year": 2022,
                "month": 12,
                "sales": 0
            },
            {
                "year": 2022,
                "month": 11,
                "sales": 0
            },
            {
                "year": 2022,
                "month": 10,
                "sales": 0
            },
            {
                "year": 2022,
                "month": 9,
                "sales": 0
            },
            {
                "year": 2022,
                "month": 8,
                "sales": 0
            },
            {
                "year": 2022,
                "month": 7,
                "sales": 0
            },
            {
                "year": 2022,
                "month": 6,
                "sales": 0
            },
            {
                "year": 2022,
                "month": 5,
                "sales": 4400
            },
            {
                "year": 2022,
                "month": 4,
                "sales": 3300
            },
            {
                "year": 2022,
                "month": 3,
                "sales": 2200
            }
        ]
        self.assertEqual(expected_data, response.data)

    def create_sale(self, customer, bike, units_sold=1, discount_percentage=0, date="2023-02-19"):
        payload = {
            "bikes": [
                {
                    "id": bike.id,
                    "unitsSold": units_sold
                },
            ],
            "customer": {
                "email": customer.email,
                "firstName": customer.first_name,
                "lastName": customer.last_name
            },
            "paymentMethod": "credit/debit",
            "date": date,
            "discountPercentage": discount_percentage
        }
        url = "/api/sales/"
        response = self.client.post(url, data=payload, format="json")
        sale = Sale.objects.get(pk=response.data["id"])
        return sale
