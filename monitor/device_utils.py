from .models import Device, DeviceUsage
from .device_usage import add_usage, close_last_device_usage, add_iddle_time

import logging 
from datetime import date, datetime, timedelta

def add_device(user, device_details) -> bool: 
    is_active = device_details['is_active']    
    last_device_usage = None
    
    fields = {
        'user': user,
        'last_device_usage': last_device_usage, 
        'device_name': device_details['device_name'], 
        'expenses': float(device_details['device_price']) + \
            float(device_details['additional_expenses']), 
        'mining_rate': device_details['mining_rate'], 
        'power_consumption': device_details['power_consumption'], 
        'buy_price': device_details['device_price'], 
        'is_active': is_active,
    }
            
    new_device = Device(**fields)
    new_device.save()
        
    if is_active: 
        # Add new usage starting from now
        usage_id = add_usage(new_device)        
        new_device.last_device_usage = usage_id
        new_device.save()
    
    return True

def device_has_unclosed_usage(device): 
    last_usage_id = Device.objects.get(pk=device.device_id).last_device_usage
    if not last_usage_id:
        return False

    return bool(DeviceUsage.objects.get(pk=device.device_id).end_time)

def get_devices(user_id, archive: bool): 
    if archive:            
            ret_columns = 'device_id', 'device_name', 'expenses', 'revenue', 'buy_price', 'sell_price'
    else:
        ret_columns = 'device_id', 'device_name', 'expenses', 'revenue', 'buy_price', 'is_active'

    devices = Device.objects.filter(is_sold=archive).values_list(*ret_columns)      

    return devices

def sell_device(device, sell_price):    
    close_last_device_usage(device)    
    device.sell_price = sell_price
    device.is_sold = True
    device.is_active = False
    device.save()

def set_device_state(device, active: bool):         
    """Change device state and open/close usage""" 
    device.is_active=active
    device.save()
    if active:
        add_usage(device)
    else:
        close_last_device_usage(device) 

def add_expenses(device, expenses):     
    device.expenses += expenses
    device.save()

def manage_devices(user, settings):     
    change = settings['manage_option']
    device_id = settings['device_id']
    try:
        device = Device.objects.get(pk=device_id)        
    except ObjectDoesNotExist:
        return False

    if change == 'sell': 
        sell_price = settings['sell_price']   
        sell_device(device, sell_price)   
    elif change == 'activate':
        set_device_state(device, True)
    elif change == 'deactivate':            
        set_device_state(device, False)    
    elif change == 'add expenses':
        expenses = float(settings['expenses'])
        add_expenses(device, expenses) 
    elif change == 'set iddle time' or change == 'set active time':           
        start_time = datetime.strptime(settings['time_start'], '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(settings['time_end'], '%Y-%m-%dT%H:%M')            
        if change == 'set iddle time':   
            add_iddle_time(device, start_time, end_time)
        else:
            add_usage(device, (start_time, end_time))
    else:            
        return False

    return True   