window.addEventListener('DOMContentLoaded', function() {        
    document.getElementById("submit").onclick = function() {        
        addDevice();    
        clearInput(['device-name', 'device-price', 'power-consumption', 
            'additional-expenses', 'mining-rate', 'hashrate-unit-options',
            'is-active']);
    }    
})

function addDevice() {
    let device_json = formToJSON(document.getElementById('form'));        
    if (!device_json) {
        printMessage('Couldn\'t add device.'); 
        console.log('No form to get data for new device')
        return;    
    }        

    setCsrfToken();
    $.ajax({
        url: '/add-device/',
        type: 'POST',
        data: JSON.stringify(device_json),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: true
    })
    .done(function(response) {        
        if (response['success']) {
            printMessage('Added device successfuly.');      
        } else { 
            printMessage('Could not add device.');      
        }        
    })
    .fail(function() { 
        printMessage('Could not add device.');      
    });    
}




