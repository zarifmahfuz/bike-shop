from graphene import relay
from graphene_django import DjangoObjectType
from .models import Bike


class BikeType(DjangoObjectType):
    class Meta:
        model = Bike
        fields = ("id", "name", "model", "price",
                  "units_available", "description", "image")
        interfaces = (relay.Node,)


class BikeConnectionType(relay.Connection):
    class Meta:
        node = BikeType
