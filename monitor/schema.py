import graphene
from graphene_django import DjangoObjectType
from .models import User, Device, DeviceUsage, Transaction

class UserType(DjangoObjectType):
    class Meta:
        model = User

class DeviceType(DjangoObjectType): 
    class Meta: 
        model = Device

class TransactionType(DjangoObjectType): 
    class Meta: 
        model = Transaction

class Query(graphene.ObjectType):    
    devices = graphene.List(
        DeviceType, 
        ids=graphene.List(graphene.Int), 
        archive=graphene.Boolean()
    )

    transactions = graphene.List(
        TransactionType, 
        ids=graphene.List(graphene.Int)
    )

    def resolve_devices(root, info, archive, ids=None):
        if ids is not None: 
            return Device.objects.filter(pk__in=ids, is_sold=archive)             
        return Device.objects.filter(is_sold=archive)
    
    def resolve_transactions(root, info, ids=None): 
        if ids is not None: 
            return Transaction.objects.filter(pk__in=ids)
        return Transaction.objects.all()

schema = graphene.Schema(query=Query)   
        