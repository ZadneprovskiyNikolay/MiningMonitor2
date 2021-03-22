var global_current_devices = {};

currentDeviceFields = [
    'deviceId', 'deviceName', 'expenses', 
    'revenue', 'buyPrice', 'isActive'
]
archiveDeviceFields = [
    'deviceId', 'deviceName', 'expenses', 
    'revenue', 'buyPrice', 'sellPrice'
]

function deviceToTableRow(device) {
    var device_name = `${device['deviceName']}(${device['deviceId']})`;
    var row = [
        device_name,
        device['expenses'], 
        device['revenue'], 
        device['buyPrice']
    ]        
    if (Boolean(device['archive'])) {
        row.push(device['sell_price']);
    } else {
        row.push(device['is_active']);
    }
    return row;
}

function loadDevicesPromise(fields, archive) {    
    return new Promise(function(resolve, reject) { 
        var query = { query: `
            query {
                devices(archive: ${archive}) {    
                    ${fields.join('\n')}
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
            resolve(r['data']['devices']); 
        })        
        .catch(error => { 
            console.error('Error loading devices: ' + error);
            reject();
        })        
    })    
}    

function fillDevicesTable(devices) { 
    if (devices.length == 0) {
        return;   
    }
    var archive = devices[0]['archive'];
    var tableElement = document.getElementById('my-table');        

    generateTableHead(tableElement, archive);
    generateTableBody(tableElement, devices);
}

function generateTableHead(table, archive, rowId='table-header') {    
    var header = null;
    if (archive)
        header = ['Device name', 'Expenses', 'Revenue', 'Buy price', 'Sell price']
    else
        header = ['Device name', 'Expenses', 'Revenue', 'Buy price', 'Is active'] 

    var thead = table.createTHead();
    var row = thead.insertRow();

    for (x of header) {
        var text = document.createTextNode(x);
        var th = document.createElement("th");
        th.appendChild(text);
        row.appendChild(th);
        row.id = rowId;           
    }
  }

function generateTableBody(table, devices) {
    var body = table.create;
    for (device of devices) {              
        var row = table.insertRow();
        row_data = deviceToTableRow(device);

        for (value of row_data) {
            var cell = row.insertCell();
            var text = document.createTextNode(value);
            cell.appendChild(text);
        }
    }
}

function loadCurrentDevices() {
    global_current_devices = {};
    loadDevicesPromise(currentDeviceFields, false)
    .then(devices => {
        for (device of devices) {             
            global_current_devices[device['deviceId']] = device;
        }                
    });    
    
}

function updateDeviceSelector(archive = false, nonarchvie = false) {        
    // Load selector from archive and/or nonarchive devices

    // Download devices info
    var devices_info = [];
    var promises = []; 
    if (archive) promises.push(loadDevicesPromise(['deviceId', 'deviceName'], false));
    if (nonarchvie) promises.push(loadDevicesPromise(['deviceId', 'deviceName'], true));    
    Promise.all(promises)
    .then(r => { 
        for (devices of r) {      
            if (devices.length != 0) {      
                devices_info.push(...devices);
            }
        }   
        
        // Update selector
        selector = document.getElementById('device-selector');
        $('#device-selector option').remove();
        for (device of devices_info) {            
            var option_text = `${device['deviceName']}(${device['deviceId']})`;
            var opt = document.createElement('option');
            opt.appendChild( document.createTextNode(option_text) );
            opt.value = device['deviceId']; 
            selector.appendChild(opt);
        }
        })       
}