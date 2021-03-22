window.addEventListener('DOMContentLoaded', onload);

function onload() {    
    loadDevicesPromise(archiveDeviceFields, true)
    .then(fillDevicesTable)
    .catch(function() {});  
}
