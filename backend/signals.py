from django.dispatch import receiver
from django.db.models.signals import pre_delete
from .models import Sale


@receiver(pre_delete, sender=Sale)
def update_bike_inventory(sender, instance, using, origin, **kwargs):
    for bike_sale in instance.bikes.all():
        bike = bike_sale.bike
        bike.units_available += (bike_sale.units_sold -
                                 bike_sale.units_refunded)
        bike.save()
