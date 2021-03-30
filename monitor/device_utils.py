from .models import Device, DeviceUsage
from .device_usage import add_usage, close_last_device_usage, add_iddle_time

import logging 
from datetime import date, datetime, timedelta

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
    device.is_active = active
    if active:
        usage_id = add_usage(device).device_usage_id        
        device.last_device_usage = usage_id
    else:
        close_last_device_usage(device) 

    device.save()

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