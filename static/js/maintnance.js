window.addEventListener('DOMContentLoaded', function() {
    $("#submit").click(function(e) {
        e.preventDefault();
        submitFun();  
        clearInput(['number-input']);
    });
})

function submitFun() {
    let form = document.getElementById('form');        
    let change_json = formToJSON(form);
    if (!change_json) return;

    // Submit change
    setCsrfToken();
    $.ajax({
        url: '/maintenance/',
        type: 'POST',
        data: JSON.stringify(change_json),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: true
    }).done(function(response) { 
        if (response['success']) {
            printMessage('Applied change successfuly.');            
        } else {
            printMessage('Couldn\'t apply change.');                
        }
    }).fail(function() { 
        printMessage('Couldn\'t apply change.');            
    })
}

function getChangeValue() { 
    return $('#maintenance-selector').val();
}