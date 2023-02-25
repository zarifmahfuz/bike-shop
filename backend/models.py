from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.shortcuts import get_object_or_404
from django.db.models import Sum, F
from . import managers
from .exceptions import RefundError


class Bike(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    units_available = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    image = models.URLField(blank=True)
    objects = managers.BikeManager()

    def __str__(self):
        return f"{self.name} - {self.model}"

    def sale_stats(self):
        query_result = self.sales.aggregate(total_sales=Sum(F('units_sold') * F('price')),
                                            units_sold=Sum('units_sold'), units_refunded=Sum('units_refunded'))
        if query_result["total_sales"] is None:
            query_result["total_sales"] = 0
            query_result["units_sold"] = 0
            query_result["units_refunded"] = 0
        return query_result


class Customer(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    objects = managers.CustomerManager()


class Sale(models.Model):
    PAYMENT_CHOICES = (
        ("cash", "Cash"),
        ("credit/debit", "Credit/Debit Card")
    )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    sold_at = models.DateField()
    updated_at = models.DateField(auto_now=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES)
    total_sale = models.DecimalField(max_digits=8, decimal_places=2)
    discount_percentage = models.IntegerField(default=0, blank=True, validators=[
        MinValueValidator(0), MaxValueValidator(100)
    ])
    objects = managers.SaleManager()

    def update(self, validated_data):
        if "discount_percentage" in validated_data:
            self.discount_percentage = validated_data["discount_percentage"]

        if "refund" in validated_data:
            refund_bikes = []
            for refund_bike in validated_data["refund"]:
                bike_sale = get_object_or_404(
                    BikeSale, bike=refund_bike["id"], sale=self.id)
                if refund_bike["units_refunded"] > bike_sale.units_sold:
                    message = f"Units refunded for {bike_sale.bike} exceed units that were originally sold."
                    raise RefundError(detail=message)
                if refund_bike["units_refunded"] < bike_sale.units_refunded:
                    message = f"You are attempting to decrease the total units refunded for {bike_sale.bike}. "\
                        "This is not allowed."
                    raise RefundError(detail=message)
                refund_bikes.append((bike_sale, refund_bike["units_refunded"]))

            for bike_sale, units_refunded in refund_bikes:
                bike = bike_sale.bike
                bike.units_available += (units_refunded -
                                         bike_sale.units_refunded)
                bike_sale.units_refunded = units_refunded
                self.total_sale -= bike_sale.price * units_refunded
                bike.save()
                bike_sale.save()
        self.save()


class BikeSale(models.Model):
    sale = models.ForeignKey(Sale, related_name="bikes",
                             on_delete=models.CASCADE)
    bike = models.ForeignKey(Bike, related_name="sales",
                             on_delete=models.PROTECT)
    units_sold = models.PositiveIntegerField(default=1)
    units_refunded = models.PositiveIntegerField(default=0, blank=True)
    price = models.DecimalField(
        "Price at which the bike was sold at", max_digits=7, decimal_places=2)
    objects = managers.BikeSaleManager()
