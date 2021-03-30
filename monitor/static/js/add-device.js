window.addEventListener('DOMContentLoaded', function() {        
    document.getElementById("submit").onclick = function() {        
        addDevice();    
        clearInput(['device-name', 'device-price', 'power-consumption', 
            'additional-expenses', 'mining-rate', 'hashrate-unit-options',
            'is-active'
        ]);
    }    
})

function addDevice() {
    // Get form data
    var deviceData = formToJSON(document.getElementById('form'));    
    if (!deviceData) {
        printMessage('Couldn\'t add device.');         
        console.log('No form to get data for new device');
        return;    
    } 
    deviceData['miningRateUnit'] = Number(deviceData['miningRateUnit']);        
    
    var mutation_params = createParamStringGraphql(deviceData);
    var mutation = {
        query: 
        `mutation FirstMutation {
            createDevice(deviceData: {${mutation_params}}) {    
                device {
                    deviceName
                }
            }
        }`
    }    
    fetch('/graphql', { 
        method: 'POST', 
        headers: { 
            'Content-Type': 'application/json', 
            'Accept': 'application/json',
            'X-CSRFToken': Cookies.get('csrftoken'), 
        }, 
        body: JSON.stringify(mutation), 
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
}




