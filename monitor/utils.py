from .models import DeviceUsage
from . import services

from django.http import HttpResponseForbidden

import logging
from collections.abc import Iterable
import datetime
from functools import wraps
import json
import datetime

logger = logging.getLogger(__name__)

def converter_json(o):
    if isinstance(o, datetime.date) or isinstance(o, datetime.datetime):
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
                if not services.check_ownership(user_id, device_id):  
                    logging.info('Access forbidden: User {} '\
                        'is attempting to get/change information '\
                        'about device {}'.format(user_id, device_id))
                    return HttpResponseForbidden()

            return view_func(request, *args, **kwargs)                           
        return _wrapped_view
    return decorator