var devices = null;

window.addEventListener('DOMContentLoaded', onload);

function onload() {                 
    // load devices and fill device selector
    loadDevicesPromise('my_devices.json', false).then(function(dv) {
        devices = dv;
        loadMyDevicesSelector(dv);
    });    
    
    $("#manage-options").change(onManageOptionChange);  
    onManageOptionChange();    
    
    // set max time-end to current time
    var max_time = new Date().toISOString().split('Z')[0]; 
    document.getElementById('time-end').max = max_time;      
    document.getElementById('time-start').max = max_time;      

    document.getElementById('apply-btn').onclick = function() {
        applyChange();
        clearInput(['time-start', 'time-end', 'sell-price', 'expenses']);
    }
}

function applyChange() {
    // Clear message field
    printMessage('');

    // load device and change
    let change_json = formToJSON(document.getElementById('form'));        
    
    if (!check_change_params(change_json)) {        
        return;
    }        

    // send change   
    setCsrfToken(); 
    $.ajax({
        url: '/manage-devices/',
        type: 'POST',
        data: JSON.stringify(change_json),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: true
    }).done(function(response) { 
        if (response['success']) {
            printMessage('Applied change successfuly');
        } else { 
            printMessage('Could not apply this change');    
        }
        loadMyDevices();
    }).fail(function() {
        printMessage('Could not apply this change');    
    });
}

function check_change_params(obj) { 
    var device = getDevice(obj['device_id']);           
    var change = obj['manage_option'];    
    var sellPrice = obj['sell_price'];
    var expenses = obj['expenses'];
    var time_start = obj['time_start']    
    var time_end = obj['time_end']    
    var isActive = device.is_active;    

    errMsg = ''
    if (!change || !device) { 
        errMsg = 'Can\'t apply this chage';
    } else if (change == 'activate' && isActive) {
        errMsg = 'Device is already active';               
    } else if (change == 'deactivate' && !isActive) { 
        errMsg = 'Device is already inactive';
    } else if (change == 'sell' && (!sellPrice || sellPrice < 0)) {
        errMsg = 'Incorrect sell price';
    } else if (change == 'add expenses' && (!expenses || expenses <= 0)) {
        errMsg = 'Incorrect expenses';      
    } else if ((change == 'set iddle time' || change == 'set active time') &&
               time_start >= time_end) {
        errMsg = 'Start date is bigger or equal to end date';      
    } else { 
        return true;
    }

    printMessage(errMsg);
    return false;
}

function getDevice(deviceId) {    
    if (!devices) return null;

    for (let x = 0; x < devices.length; ++x) {
        let devicex = devices[x];
        if (devicex.deviceId == deviceId) {
            return devicex;
        }
    }

    return null;
}

function printMessage(msg) {    
    document.getElementById('message').innerHTML = msg;
}

function createUrlParamsString(params) {
    let str = '';
    for (param in params) {
        str += param + '=' + encodeURIComponent(params[param]) + '&'
    }

    return str;
}

function onManageOptionChange() { 
    if ($("#manage-options").val() == "sell") {
        $(".on-sell-show").show();        
    } else {
        $(".on-sell-show").hide();
    }

    if ($("#manage-options").val() == "add expenses") {
        $(".on-add-expenses-show").show();   
    } else {
        $(".on-add-expenses-show").hide();   
    }

    if ($("#manage-options").val() == "set iddle time" || 
        $("#manage-options").val() == "set active time") 
    {
        $(".on-set-time-show").show();   
    } else {
        $(".on-set-time-show").hide();   
    }    
}