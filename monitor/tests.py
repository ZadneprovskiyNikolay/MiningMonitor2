from .models import DeviceUsage
from . import device_utils

from django.contrib.auth.models import User
from django.test import TestCase

from datetime import datetime, timedelta

new_device_fields = {         
    'device_name': 'Test device',     
    'device_price': 1000, 
    'additional_expenses': 100, 
    'mining_rate': 97, 
    'power_consumption': 300, 
    'sell_price': 0, 
    'is_sold': False, 
    'is_active': False
}

def create_user(username, password): 
    user = User.objects.create_user(username=username, password=password)        
    user.save() 
    return user

class DeviceUsageTests(TestCase): 
    def test_overlapping_usages_concatenate(self): 
        user = create_user('root', 'root') 
        device = device_utils.add_device(user, new_device_fields)        
        time_now = datetime.now()
        time_10_days_ago = time_now + timedelta(days=-10)
        time_11_days_ago = time_now + timedelta(days=-11)
        time_19_days_ago = time_now + timedelta(days=-19)
        time_20_days_ago = time_now + timedelta(days=-20)
        time_30_days_ago = time_now + timedelta(days=-30)

        device_utils.add_usage(device, (time_20_days_ago, time_10_days_ago))
        usage = device_utils.add_usage(device, (time_30_days_ago, time_19_days_ago))        
        concatenated = bool(DeviceUsage.objects.filter(
            start_time=time_30_days_ago, end_time=time_10_days_ago))
        self.assertEqual(concatenated, True)

        usage = device_utils.add_usage(device, (time_11_days_ago, time_now))
        print(usage)
        concatenated = bool(DeviceUsage.objects.filter(
            start_time=time_30_days_ago, end_time=time_now))
        self.assertEqual(concatenated, True)

    def test_adding_usage_updates_last_usage_id(self): 
        user = create_user('root', 'root') 
        device = device_utils.add_device(user, new_device_fields)   
        
        usage = device_utils.add_usage(device, 
            (datetime.now() + timedelta(days=-10), 
            datetime.now() + timedelta(days=-5)))
        self.assertEqual(usage.device_usage_id, device.last_device_usage)

        usage = device_utils.add_usage(device, 
            (datetime.now() + timedelta(days=-3), datetime.now()))
        self.assertEqual(usage.device_usage_id, device.last_device_usage)
        
        


    
