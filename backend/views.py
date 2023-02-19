from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from . import serializers
from .models import Bike, Customer, Sale


class BikesView(APIView):
    def get(self, request):
        if "search" in request.query_params:
            queryset = Bike.objects.with_match(
                request.query_params["search"]).all()
        else:
            queryset = Bike.objects.all()
        serializer = serializers.BikeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = serializers.BikeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class BikeView(APIView):
    def get(self, request, id):
        bike = get_object_or_404(Bike, pk=id)
        serializer = serializers.BikeSerializer(bike)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        bike = get_object_or_404(Bike, pk=id)
        serializer = serializers.BikeSerializer(instance=bike,
                                                data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class CustomersView(APIView):
    def get(self, request):
        if "email" in request.query_params:
            queryset = Customer.objects.with_email(
                email=request.query_params["email"]).all()
        else:
            queryset = Customer.objects.all()
        serializer = serializers.CustomerSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = serializers.CustomerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomerView(APIView):
    def get(self, request, id):
        customer = get_object_or_404(Customer, pk=id)
        serializer = serializers.CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SalesView(APIView):
    def get(self, request):
        serializer = serializers.SaleSerializer(Sale.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = serializers.CreateSaleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            sale = serializer.save()
            serializer = serializers.SaleSerializer(sale)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class SaleView(APIView):
    def get(self, request, id):
        sale = get_object_or_404(Sale, pk=id)
        serializer = serializers.SaleSerializer(sale)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        pass

    def delete(self, request, id):
        pass
