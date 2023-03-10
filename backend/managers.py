from django.db import models as django_models
from django.shortcuts import get_object_or_404
from django.db.models import Sum, F, DecimalField
from django.db.models.functions import Cast, ExtractYear, ExtractMonth
from django.utils.timezone import now, timedelta
from . import models
from .exceptions import NotEnoughBikeUnitsAvailable
from .utils import get_years_months


class BikeManager(django_models.Manager):
    def with_match(self, search_string):
        queryset = self.get_queryset()
        match_name = queryset.filter(name__contains=search_string)
        match_model = queryset.filter(model__contains=search_string)
        return match_name.union(match_model)

    def top_selling_bikes(self, limit=10):
        top_bikes = self.annotate(
            total_sales=Sum(F('sales__units_sold') * F('sales__price'))).order_by('-total_sales')
        total_sales_over_all_bikes = top_bikes.aggregate(Sum('total_sales'))
        top_bikes = top_bikes.annotate(
            sales_percentage=Cast(F('total_sales') * 100 / total_sales_over_all_bikes["total_sales__sum"], output_field=DecimalField()))
        return top_bikes[:limit]


class CustomerManager(django_models.Manager):
    def with_email(self, email):
        return self.get_queryset().filter(email__contains=email)


class SaleManager(django_models.Manager):
    def create(self, serializer_data):
        total_sale = 0
        bikes = []
        for bike in serializer_data["bikes"]:
            bike_object = get_object_or_404(models.Bike, pk=bike["id"])
            if bike_object.units_available < bike["units_sold"]:
                message = f"{bike['units_sold']} units are not available for {bike_object}. "\
                    "Please ensure that bikes have enough stock before making a sale."
                raise NotEnoughBikeUnitsAvailable(detail=message)
            total_sale += bike_object.price * bike["units_sold"]
            bikes.append((bike_object, bike["units_sold"]))

        customer = models.Customer.objects.get_or_create(
            email=serializer_data["customer"]["email"], defaults=serializer_data["customer"])[0]
        sale = models.Sale(customer=customer, sold_at=serializer_data["date"], payment_method=serializer_data["payment_method"],
                           total_sale=round(total_sale, 2), discount_percentage=serializer_data["discount_percentage"])
        sale.save()
        for bike, units_sold in bikes:
            bike.units_available -= units_sold
            models.BikeSale.objects.create(
                sale=sale, bike=bike, units_sold=units_sold, price=bike.price)
            bike.save()
        return sale

    def with_customer_email(self, email):
        return self.get_queryset().filter(customer__email__contains=email).order_by("-sold_at")

    def with_bike(self, bike):
        queryset = self.get_queryset()
        match_bike_name = queryset.filter(bikes__bike__name__contains=bike)
        match_bike_model = queryset.filter(bikes__bike__model__contains=bike)
        return match_bike_name.union(match_bike_model).order_by("-sold_at")

    def total_discount(self):
        queryset = self.annotate(discount=Cast(
            F('total_sale') * F('discount_percentage') / 100.0, output_field=DecimalField()))
        return queryset.aggregate(Sum('discount'))['discount__sum']

    def total_sales(self):
        return self.aggregate(Sum('total_sale'))['total_sale__sum']

    # Returns a list of (year, month, sales) for the last 12 months
    def monthly_sales(self):
        today = now().date()
        last_12_months = get_years_months(today, 12)

        one_year_ago = today - timedelta(days=365)
        sales_by_month = self.filter(
            sold_at__gte=one_year_ago,
            sold_at__lte=today
        ).annotate(
            year=ExtractYear('sold_at'),
            month=ExtractMonth('sold_at')
        )

        monthly_sales = sales_by_month.values('year', 'month').annotate(
            total_sales=Sum('total_sale')
        ).order_by('year', 'month')

        sales_by_month = [(y, m, next(
            (s['total_sales'] for s in monthly_sales if (s['year']) == y and s['month'] == m), 0)) for (y, m) in last_12_months]
        return sales_by_month


class BikeSaleManager(django_models.Manager):
    def total_bikes_sold(self):
        return self.aggregate(Sum('units_sold'))['units_sold__sum']

    def total_bikes_refunded(self):
        return self.aggregate(Sum('units_refunded'))['units_refunded__sum']
