from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Device(models.Model): 
    device_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_device_usage = models.IntegerField(null=True, blank=True)
    device_name = models.CharField(max_length=255)
    expenses = models.FloatField()
    revenue = models.FloatField(default=0)
    mining_rate = models.IntegerField()
    power_consumption = models.IntegerField()
    buy_price = models.FloatField()
    sell_price  = models.FloatField(default=0)
    is_sold = models.BooleanField(default=False)
    is_active = models.BooleanField()

    class Meta: 
        db_table = 'device_list' 

class DeviceUsage(models.Model):
    device_usage_id = models.AutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)

    class Meta:
        db_table = 'device_usage'        

    def __str__(self): 
        return f'({self.start_time}, {self.end_time})'

    def usage_range(self): 
        return self.start_time, self.end_time
  
class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.FloatField()

    class Meta: 
        db_table = 'transaction'    

    def date_amount(self): 
        return self.date, self.amount

class PowerCost(models.Model): 
    power_cost_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cost_per_watH = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    
    class Meta: 
            db_table = 'power_cost'

