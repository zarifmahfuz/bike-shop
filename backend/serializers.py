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


class CreateBikeSaleSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    units_sold = serializers.IntegerField(min_value=0, required=True)


class BikeSaleSerializer(serializers.ModelSerializer):
    bike = BikeSerializer()

    class Meta:
        model = models.BikeSale
        fields = ["bike", "units_sold", "units_refunded", "price"]


class CreateSaleSerializer(serializers.ModelSerializer):
    bikes = CreateBikeSaleSerializer(many=True)
    customer_id = serializers.IntegerField(required=True)
    date = serializers.DateField(required=True)

    class Meta:
        model = models.Sale
        fields = ["bikes", "customer_id",
                  "discount_percentage", "payment_method", "date"]

    def create(self, validated_data):
        return models.Sale.objects.create(validated_data)


class SaleSerializer(serializers.ModelSerializer):
    bikes = BikeSaleSerializer(many=True)
    customer = CustomerSerializer()

    class Meta:
        model = models.Sale
        fields = ["id", "net_sale", "discount_percentage",
                  "sold_at", "updated_at", "customer", "bikes"]
