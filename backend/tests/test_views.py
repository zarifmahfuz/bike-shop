from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Bike, Customer, Sale


class SalesTestCase(APITestCase):
    def test_create_sale(self):
        customer = Customer.objects.create(
            first_name="Michael", last_name="Bisping", email="bisping@gmail.com")
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
            "customerId": customer.id,
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
        self.assertEqual(customer.id, response.data["customer"]["id"])

        # test the model data
        bike_1.refresh_from_db()
        bike_2.refresh_from_db()
        self.assertEqual(1, bike_1.units_available)
        self.assertEqual(1, bike_2.units_available)

    def test_create_sale_with_insufficient_stock(self):
        customer = Customer.objects.create(
            first_name="Michael", last_name="Bisping", email="bisping@gmail.com")
        bike = Bike.objects.create(
            name="Trek Marlin", model="Trek Marlin 6", price=1049.99, units_available=2)
        payload = {
            "bikes": [
                {
                    "id": bike.id,
                    "unitsSold": 3
                }
            ],
            "customerId": customer.id,
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
        customer = Customer.objects.create(
            first_name="Michael", last_name="Bisping", email="bisping@gmail.com")
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
            "customerId": customer.id,
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
            "customerId": customer.id,
            "paymentMethod": "credit/debit",
            "date": "2023-02-19",
            "discountPercentage": discount_percentage
        }
        url = "/api/sales/"
        response = self.client.post(url, data=payload, format="json")
        sale = Sale.objects.get(pk=response.data["id"])
        return sale
