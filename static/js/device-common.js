class Device { 
    constructor(db_row, archive) {
        this.archive = archive
        this.deviceId = db_row[0]; 
        this.device_name = db_row[1]; 
        this.expenses = db_row[2];
        this.revenue = db_row[3];
        this.buy_price = db_row[4];    
        if (archive) {
            this.sell_price = db_row[5]                        
        } else {
            this.is_active = db_row[5]
        }
    }    

    toTableRow(active) {
        var device_name = String(this.device_name) + '(' + this.deviceId + ')'
        var row = [
            device_name,
            this.expenses, 
            this.revenue, 
            this.buy_price
        ]        
        if (this.archive) {
            row.push(this.sell_price)
        } else {
            row.push(this.is_active)
        }

        return row;
    }
}

function loadDevicesPromise(file_name, archive) {  
    return new Promise(function (resolve, reject) {
        $.getJSON('/devices/' + file_name).done(function(data, textStatus, jqXHR) { 
            devices = []      
            for (device_data of data) {
                devices.push(new Device(device_data, archive));
            }    
            resolve(devices);
        }).fail(function(jqxhr, textStatus, error) {
            console.error('Error loading devices: ' + error);
            reject();
        });
    })        
}    

function fillDevicesTable(devices) { 
    if (devices.length == 0) {
        return;   
    }
    var archive = devices[0].archive
    var tableElement = document.getElementById('my-table');        

    generateTableHead(tableElement, archive);
    generateTableBody(tableElement, devices);
}

function generateTableHead(table, archive, rowId='table-header') {    
    var header = null
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
    var body = table.create
    for (device of devices) {              
        var row = table.insertRow();
        row_data = device.toTableRow();

        for (value of row_data) {
            var cell = row.insertCell();
            var text = document.createTextNode(value);
            cell.appendChild(text);
        }
    }
}

function loadMyDevices() {
    loadDevicesPromise('my_devices.json', false).then(function(dv) {
        devices = dv;
    });    
}

function loadMyDevicesSelector(devices) {        
    selector = document.getElementById('device-selector');

    for (device of devices) {
        var option_text = String(device.device_name) + '(' + device.deviceId + ')';
        var opt = document.createElement('option');
        opt.appendChild( document.createTextNode(option_text) );
        opt.value = device.deviceId; 
        selector.appendChild(opt);
    }
}   