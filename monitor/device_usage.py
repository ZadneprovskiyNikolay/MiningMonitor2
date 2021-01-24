from .models import Device, DeviceUsage, PowerCost

from django.core.exceptions import ObjectDoesNotExist

import logging 
from collections.abc import Iterable
from datetime import datetime, date, time, timedelta

logger = logging.getLogger(__name__)

def add_usage(device, time_range: Iterable[datetime] = None):        
    if time_range is None:         
        # Open new usage with start_time = now
        start_time = datetime.now()              

        if device_has_unclosed_usage(device):            
            raise Exception('Can not add new device usage for device_id = {} '\
                            'while previous one is nomodels.DateField(),  closed'.format(device.device_id))        

        # Open new usage            
        usage_id = DeviceUsage.objects.create(device=device, start_time=start_time).device_usage_id
        # Set last_device_usage for current device
        device.last_device_usage=usage_id
        device.save()

        return True        
    else:              
        start_time, end_time = time_range

        # Don't do anything if usage in range (start_time, end_time) exists
        if DeviceUsage.objects.filter(device=device, 
            start_time__lte=start_time, 
            end_time__gte=end_time).exists():                                 
            return

        # Delete all usages in range (start_time, end_time)            
        DeviceUsage.objects.filter(device=device, 
            start_time__gte=start_time, 
            end_time__lte=end_time).delete()

        # Delete usages overlapping range (start_time, end_time) and 
        # set new start_time and end_time
        try:
            usage_overlapping_start = DeviceUsage.objects.get(device=device, 
                end_time__gte=start_time, 
                end_time__lte=end_time)
            start_time = usage_overlapping_start.start_time 
            usage_overlapping_start.delete()
        except ObjectDoesNotExist:
            pass        

        try:
            usage_overlapping_end = DeviceUsage.objects.get(device=device, 
                start_time__gte=start_time, 
                start_time__lte=end_time)
            end_time = usage_overlapping_end.start_time            
            usage_overlapping_end.delete()
        except ObjectDoesNotExist:
            pass      
        
        # Add usage
        DeviceUsage.objects.create(device=device, 
            start_time=start_time, end_time=end_time)       

def close_last_device_usage(device):     
    device.end_time=datetime.now()
    device.save()

def add_iddle_time(device, iddle_start, iddle_end):                    
    try: 
        containing_usage = DeviceUsage.objects.get(device=device, 
            start_time__lte=iddle_start, 
            end_time__gte=iddle_end)
    except DeviceUsage.DoesNotExist: 
        containing_usage = None

    # if iddle interval is inside closed usage interval split usage interval in two
    if containing_usage:         
        DeviceUsage.objects.create(device=device, 
            start_time=iddle_end, 
            end_time=containing_usage.end_time)                
        containing_usage.end_time = iddle_start
        containing_usage.save()
    else:         
        # delete all usage intervals inside iddle interval
        DeviceUsage.objects.filter(device=device, 
            start_time__gte=iddle_start, end_time__lte=iddle_end).delete()            
        # set new end_time/start_time for usage intervals overlapping iddle interval
        DeviceUsage.objects.filter(device=device, 
            end_time__gt=iddle_start, 
            end_time__lt=iddle_end).update(end_time=iddle_start)                    
        DeviceUsage.objects.filter(device=device, 
            start_time__gt=iddle_start, 
            start_time__lt=iddle_end).update(start_time=iddle_end)     