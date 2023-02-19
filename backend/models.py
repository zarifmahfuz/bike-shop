from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from . import managers


class Bike(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    units_available = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    image = models.URLField(blank=True)
    objects = managers.BikeManager()


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


class BikeSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT)
    bike = models.ForeignKey(Bike, on_delete=models.PROTECT)
    units = models.PositiveIntegerField(default=1)
    net_sale = models.DecimalField(
        "net_sale = sale value - discount applied", max_digits=8, decimal_places=2)
    refund = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, blank=True)
    discount_percentage = models.IntegerField(default=0, blank=True, validators=[
        MinValueValidator(0), MaxValueValidator(100)
    ])
