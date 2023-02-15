from django.contrib import admin
from .models import Bike, Customer, BikeSale, Sale

# Register your models here.
admin.site.register(Bike)
admin.site.register(Customer)
admin.site.register(BikeSale)
admin.site.register(Sale)
