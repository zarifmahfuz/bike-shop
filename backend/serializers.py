from rest_framework import serializers
import decimal
from . import models


class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bike
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = models.Customer
        fields = "__all__"


class CreateBikeSaleSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    units_sold = serializers.IntegerField(min_value=0, required=True)


class RefundBikeSaleSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    units_refunded = serializers.IntegerField(min_value=1, required=True)


class BikeSaleSerializer(serializers.ModelSerializer):
    bike = BikeSerializer()

    class Meta:
        model = models.BikeSale
        fields = ["bike", "units_sold", "units_refunded", "price"]


class CreateSaleSerializer(serializers.ModelSerializer):
    bikes = CreateBikeSaleSerializer(many=True)
    customer = CustomerSerializer(required=True)
    date = serializers.DateField(required=True)

    class Meta:
        model = models.Sale
        fields = ["bikes", "customer",
                  "discount_percentage", "payment_method", "date"]

    def create(self, validated_data):
        return models.Sale.objects.create(validated_data)


class UpdateSaleSerializer(serializers.ModelSerializer):
    refund = RefundBikeSaleSerializer(many=True, required=False)

    class Meta:
        model = models.Sale
        fields = ["discount_percentage", "refund"]

    def update(self, instance, validated_data):
        instance.update(validated_data)
        return instance


class SaleSerializer(serializers.ModelSerializer):
    bikes = BikeSaleSerializer(many=True)
    customer = CustomerSerializer()

    class Meta:
        model = models.Sale
        fields = ["id", "total_sale", "discount_percentage",
                  "sold_at", "updated_at", "customer", "bikes"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["net_sale"] = round(instance.total_sale - decimal.Decimal(
            instance.discount_percentage / 100) * instance.total_sale, 2)
        return data


class BikeAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bike
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        output_data = {"bike": data, "sales": instance.total_sales,
                       "percentage_total_sales": instance.sales_percentage}
        return output_data
