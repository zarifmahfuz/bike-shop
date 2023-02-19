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
                         response.data["net_sale"])
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
        self.assertEqual(str(expected_net_sale), response.data["net_sale"])
