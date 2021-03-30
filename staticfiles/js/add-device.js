window.addEventListener('DOMContentLoaded', function() {        
    document.getElementById("submit").onclick = function() {        
        addDevice();    
        clearInput(['device-name', 'device-price', 'power-consumption', 
            'additional-expenses', 'mining-rate', 'hashrate-unit-options',
            'is-active']);
    }    
})

function addDevice() {
    var device_data = formToJSON(document.getElementById('form'));    
    var params = Object.keys(device_data);
    var device_key_value_pairs = [];
    for (param in params) { 
        device_key_value_pairs.push(`${param}: ${device_data[param]}`)        
    }
    var device_params_string = ', '.join(device_key_value_pairs);

    if (!device_data) {
        printMessage('Couldn\'t add device.'); 
        console.log('No form to get data for new device')
        return;    
    }        

    var query = { query: `
        mutation FirstMutation {
            createDevice(deviceData: {${device_params_string}}) {    
                book {
                    ${params.join(',\n')}
                }
            }
        }
    `};

    fetch('/graphql', { 
        method: 'POST', 
        headers: { 
            'Content-Type': 'application/json', 
            'Accept': 'application/json',
            'X-CSRFToken': Cookies.get('csrftoken'), 
        }, 
        body: JSON.stringify(query), 
    })
    .then(r => r.json())
    .then(r => {            
        if (r['success']) {
            printMessage('Added device successfuly.');      
        } else { 
            printMessage('Could not add device.');      
        }   
    })        
    .catch(error => { 
        printMessage('Could not add device.');    
    })    

    // setCsrfToken();   
}




