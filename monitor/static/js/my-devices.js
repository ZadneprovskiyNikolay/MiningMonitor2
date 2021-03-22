window.addEventListener('DOMContentLoaded', onload);

function onload() {
    loadDevicesPromise(currentDeviceFields, false)
    .then(fillDevicesTable)
    .catch(function() {});      
}