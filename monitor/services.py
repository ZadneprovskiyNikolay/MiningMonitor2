from .models import Device, DeviceUsage, Transaction, PowerCost
from .utils import close_usages, has_power_cost

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Q, Min

import logging 
from collections.abc import Iterable
from datetime import datetime, date, time, timedelta

logger = logging.getLogger(__name__)                  
    
def get_work_archive(device_id): 
    """Returns: dict of time worked each day, every month is present with days >= 0
    {
        year: { 
            mounth: {day: % of time worked}
        }
    }"""
    res_dict = {}

    # Get usages sorted from the oldest to newest and set 
    # 'end_time' where it's None        
    usage_set = DeviceUsage.objects.filter(device_id=device_id).order_by('start_time')      
    if not usage_set: 
        return {}
    close_usages(usage_set)
    
    # Iterate usages and fill result_dict
    for start_time, end_time in (usage.usage_range() for usage in usage_set):
        # Add all years and months from start_time to end_time
        for year in range(start_time.year, end_time.year + 1):
            # add new year to dict 
            if res_dict.get(year, None) is None:
                res_dict[year] = {month_num:dict() for month_num in range(1, 13)}

        # Fill result dict
        work_day_start = start_time          
        while work_day_start < end_time:
            new_day = datetime.combine(work_day_start + timedelta(days=1), 
                time.min) # 00:00
            work_day_end = new_day if end_time >= new_day else end_time
            part_of_day_worked = (work_day_end - work_day_start).total_seconds() / 86400
            percent_of_day_worked = round(part_of_day_worked * 100, 1)
            res_dict[work_day_start.year][work_day_start.month][work_day_start.day] = \
                percent_of_day_worked
                                
            work_day_start = work_day_end 

    return res_dict                 

def calc_payback(user_id): 
    """Returns: device payback dict, no entries for devices that was not used yet.
    { 
        device_id: ( (date, payback %), ...), 
        ... 
    }

    Iterate through all periods between transactions, 
    get relative value of contribution(0.0-1.0) for every device 
    was working in period, then compute profit(transaction * contribution)
    from it and assign each device it's new payback in %(transaction_date, new_payback_%)
    """    

    transactions = Transaction.objects.filter(user_id=user_id).order_by('date') 
    devices_dict = {device.device_id: device for device in Device.objects.filter(user_id=user_id)}        
    devices_id = devices_dict.keys()
    if not transactions or not devices_dict: 
        return {} 
    
    # Load power cost
    power_cost = 0
    if has_power_cost(user_id): 
        power_cost = PowerCost.objects.get(user_id=user_id, end_date=None).cost_per_watH        
    
    # Start of exploitetion
    # devices_exp_start = { {device_id: 1, exp_start: datetime.datetiem(2020, 1, 1, 0, 0)}, ...}
    devices_exp_start = DeviceUsage.objects.values('device_id').annotate(exp_start=Min('start_time'))

    result_dict = {}                                  
    # Set first value(start_date, 0%) for every device in res_dict                      
    for device_exp_start in devices_exp_start:        
        device_id = device_exp_start['device_id']
        usage_start_date = device_exp_start['exp_start'].date() # Convert datetime to date
        result_dict[device_id] = [(usage_start_date, 0)]    
    
    # Main loop over all periods between transactions for 
    # devices that was active: relative contribution -> absolute pofit -> new payback % 
    period_start = datetime.min
    for trans in transactions:        
        period_end = datetime.combine(trans.date, datetime.min.time()) # Convert date to datetime
        logger.debug(f'considering period between transactions: ({period_start}, {period_end})')

        # All usages from period 
        period_usage_dict = get_usages(user_id=user_id, start_time=period_start, 
            end_time=period_end, set_usage_end=True)    
        logger.debug(f'all usages from period: {period_usage_dict}')    

        #  Get usage hours for every device in period and set its contribution(usage_hours * hashrate)
        usage_hours_dict = {}
        contrib_dict = {} # Contribution of devices                    
        for device_id in period_usage_dict:                
            device = devices_dict[device_id]                                
            usage_hours = sum((usage_end - usage_start).total_seconds() / 3600 for usage_start, usage_end in period_usage_dict[device_id])                
            usage_hours_dict[device_id] = usage_hours
            contrib_dict[device_id] = usage_hours * device.mining_rate

        # Relative contribution
        contr_sum = sum( (contrib_dict[device_id] for device_id in contrib_dict) )
        rel_contrib_dict = {device_id: (contrib_dict[device_id] / contr_sum) for device_id in contrib_dict}            
        
        # Calculate new payback % for every device(last_payback + (revenue - maintenance))
        for device_id in rel_contrib_dict:
            device = devices_dict[device_id]
            expenses = device.expenses
            revenue = rel_contrib_dict[device_id] * trans.amount
            maintenance = device.power_consumption * \
                usage_hours_dict[device_id] * power_cost
            profit = revenue - maintenance
            last_device_payback = result_dict[device_id][-1][1] # in %            
            new_payback = last_device_payback + (profit / expenses) * 100
            new_payback = round(new_payback, 2)
            result_dict[device_id].append((trans.date, new_payback))

        period_start = period_end

    return result_dict

def get_usages(devices_id: Iterable[int] = None, user_id=None,
        start_time=None, end_time=None, set_usage_end=True): 
    """                    
    Input: (devices_id
    Returns: dictionary of usages for devices from devices_id or, if None, 
        for all user_id devices touching range (start_time, end_time). If set_usage_end=True
        then usages with end_time=None are set to end_time=datetime.now()
        {device_id: ( (start_time, end_time), ...)}
    """                      
    res_dict = {}    
    
    if devices_id is None:         
        # Devices of user_id
        devices_id = tuple(Device.objects.values_list('device_id', flat=True).filter(user_id=user_id))        
                
    # Range of all time
    if start_time is None: 
        for device_id in devices_id: 
            usages = DeviceUsage.objects.filter(device_id=device_id).order_by('start_time')
            if not usages: 
                continue
            if set_usage_end: 
                close_usages(usages)
            res_dict[device_id] = tuple(usage.usage_range() for usage in usages)
    # In range (start_time, end_time)            
    else: 
        for device_id in devices_id: 
            usages = DeviceUsage.objects.filter(
                Q(device_id=device_id),
                Q(  Q( Q(end_time__isnull=True) & Q(start_time__lt=end_time)) |
                    Q( Q(start_time__lte=start_time) & Q(end_time__gt=start_time) ) |
                    Q( Q(start_time__lt=end_time) & Q(end_time__gt=end_time) )  
                )).order_by('start_time')
            if not usages: 
                continue
            if set_usage_end: 
                close_usages(usages)
            res_dict[device_id] = tuple(usage.usage_range() for usage in usages)
    
    return res_dict            

