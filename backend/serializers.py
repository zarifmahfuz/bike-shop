from rest_framework import serializers
from . import models


class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bike
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = "__all__"
