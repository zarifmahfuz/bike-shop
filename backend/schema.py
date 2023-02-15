from graphene import relay, ObjectType, Schema, List
from .types import BikeType, BikeConnectionType
from .models import Bike


class Query(ObjectType):
    bikes = relay.ConnectionField(BikeConnectionType)

    def resolve_bikes(root, info, **kwargs):
        return Bike.objects.all()


class Mutation(ObjectType):
    pass


schema = Schema(query=Query)
