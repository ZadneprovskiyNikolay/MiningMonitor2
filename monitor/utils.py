from .models import Device, DeviceUsage, PowerCost, Transaction

from django.http import HttpResponseForbidden

import logging
from collections.abc import Iterable
from functools import wraps
import json
from datetime import datetime, date

logger = logging.getLogger(__name__)

def converter_json(o):
    if isinstance(o, date) or isinstance(o, datetime):
        return o.__str__()

def close_usages(usages: Iterable[DeviceUsage]):         
    for usage in usages: 
            if usage.end_time is None: 
                usage.end_time = datetime.now() 

def ownership_required(methods=[]):
    """View decorator factory for checking ownership of device, 
    you should provide 'device_id' parameter for function
    decorated or have 'device-id' key in request.json. 
    You can specify which methods will triger check in 'methods'
    iterable(all by defauld)"""  
    def decorator(view_func):                               
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):                                                  
            if request is not None and (methods is None or request.method in methods):                                                           
                # Get device id as json field or as function argument parsed from url
                device_id = kwargs.get('device_id', None)
                if device_id is not None:
                    device_id = int(device_id)
                else:                     
                    json_data = json.loads(request.body)                    
                    device_id = json_data.get('device_id', None)                                                                                            
                
                if device_id is None:
                    logging.error('Can not retrieve device_id from funciton '\
                        'arguments or request.json (function: {})'.format(view_func.__name__))
                    return HttpResponseForbidden()
                                    
                user_id = request.user.id  
                if not check_ownership(user_id, device_id):  
                    logging.info('Access forbidden: User {} '\
                        'is attempting to get/change information '\
                        'about device {}'.format(user_id, device_id))
                    return HttpResponseForbidden()

            return view_func(request, *args, **kwargs)                           
        return _wrapped_view
    return decorator

def device_has_unclosed_usage(device): 
    last_usage_id = Device.objects.get(pk=device.device_id).last_device_usage
    if not last_usage_id:
        return False

    return not bool(DeviceUsage.objects.get(pk=device.last_device_usage).end_time)

def has_power_cost(user_id): 
    return PowerCost.objects.filter(user_id=user_id).exists()

def check_ownership(user_id, device_id):
    return Device.objects.filter(user_id=user_id, device_id=device_id).exists()

def add_transaction(user, trans_details):
    Transaction.objects.create(user=user, **trans_details)   

def get_transactions(user_id) -> tuple[tuple[datetime.date, float]]: 
    transactions = Transaction.objects.filter(user_id=user_id).order_by('-date')
    date_amount_pairs = tuple(transaction.date_amount() for transaction in transactions)
    return date_amount_pairs 

def set_maintenance_cost(user, maintenance_settings): 
    change = maintenance_settings['maintenance_option']
    value = maintenance_settings['value']  
    
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