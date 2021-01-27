window.addEventListener('DOMContentLoaded', onload);

function onload() {    
    loadDevicesPromise('archive_devices.json', true)
    .then(fillDevicesTable)
    .catch(function() {});  
}
