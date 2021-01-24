window.addEventListener('DOMContentLoaded', onload);

function onload() {
    loadDevicesPromise('my_devices.json', false)
    .then(fillDevicesTable)
    .catch(function() {});      
}
