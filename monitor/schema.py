from datetime import date

import graphene
from graphene_django import DjangoObjectType
from .models import User, Device, DeviceUsage, Transaction, PowerCost

class UserType(DjangoObjectType):
    class Meta:
        model = User

class DeviceType(DjangoObjectType): 
    class Meta: 
        model = Device
        fields = "__all__"

class TransactionType(DjangoObjectType): 
    class Meta: 
        model = Transaction

class PowerCostType(DjangoObjectType): 
    class Meta: 
        model = PowerCost
        
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
        user_id = info.context.user.id
        if ids is not None: 
            return Device.objects.filter(pk__in=ids, user=user_id, is_sold=archive)             
        return Device.objects.filter(user=user_id, is_sold=archive)
    
    def resolve_transactions(root, info, ids=None): 
        user_id = info.context.user.id
        if ids is not None: 
            return Transaction.objects.filter(user=user_id, pk__in=ids)
        return Transaction.objects.filter(user=user_id)

class DeviceData(graphene.InputObjectType):     
    device_name = graphene.String()
    buy_price = graphene.Int()
    power_consumption = graphene.Int()
    additional_expenses = graphene.Int()
    mining_rate = graphene.Int()
    mining_rate_unit = graphene.Int()
    is_active = graphene.Boolean()
    is_sold = graphene.Boolean()

class CreateDevice(graphene.Mutation): 
    class Arguments: 
        device_data = DeviceData(required=True)
        
    device = graphene.Field(DeviceType)

    @staticmethod
    def mutate(root, info, device_data=None): 
        is_active = device_data['is_active']    
        last_device_usage = None
        
        fields = {
            'user': info.context.user,
            'last_device_usage': last_device_usage, 
            'device_name': device_data['device_name'], 
            'expenses': float(device_data['buy_price']) + \
                float(device_data['additional_expenses']), 
            'mining_rate': device_data['mining_rate'], 
            'power_consumption': device_data['power_consumption'], 
            'buy_price': device_data['buy_price'], 
            'is_active': is_active,
        }
                
        new_device = Device(**fields)
        new_device.save()
            
        if is_active: 
            # Add new usage starting from now
            usage_id = add_usage(new_device).device_usage_id        
            new_device.last_device_usage = usage_id
            new_device.save()
        
        return new_device

class TransactionData(graphene.InputObjectType):     
    amount = graphene.Float()
    date = graphene.Date()

class CreateTransaction(graphene.Mutation): 
    class Arguments: 
        transaction_data = TransactionData(required=True)
        
    transaction = graphene.Field(TransactionType)

    @staticmethod
    def mutate(root, info, transaction_data=None): 
        user_id = info.context.user
        return Transaction.objects.create(user=user_id, **transaction_data)                     

class PowerCostData(graphene.InputObjectType): 
    maintenance_option = graphene.String()
    value = graphene.Float()

class SetPowerCost(graphene.Mutation): 
    class Arguments: 
        power_cost = PowerCostData(required=True)
        
    power_cost = graphene.Field(PowerCostType)
    
    @staticmethod
    def mutate(root, info, power_cost=None): 
        change = power_cost['maintenance_option']
        value = power_cost['value']  
        user = info.context.user

        if change == 'electricity':
            today_date = date.today()
            value = float(value) / 1000 # $/KW/H -> $/W/H            
            fields = { 
                'user': user, 
                'cost_per_watH': value, 
                'start_date': today_date
            }
            if PowerCost.objects.filter(user=user).exists():            
                PowerCost.objects.filter(user=user).update(end_date=today_date)
            PowerCost.objects.create(**fields)
        else: 
            return False
        return True

class Mutation(graphene.ObjectType): 
    create_device = CreateDevice.Field()
    create_transaction = CreateTransaction.Field()
    set_power_cost = SetPowerCost.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)   

