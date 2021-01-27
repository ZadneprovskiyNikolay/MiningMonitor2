window.addEventListener('DOMContentLoaded', function() {
    // set max transaction-time to current time
    var max_time = new Date().toISOString().split('Z')[0]; 
    document.getElementById('transaction-date').max = max_time;          

    $("#submit").click(function(e) {
        e.preventDefault();        
        submitFun();    
        clearInput(['transaction-value', 'transaction-date']);
    })
})

function submitFun() {
    let form = document.getElementById('form');    
    let transaction_json = formToJSON(form);
    if (!transaction_json) return;

    // apply    
    setCsrfToken();
    $.ajax({
        url: '/add-transaction/',
        type: 'POST',
        data: JSON.stringify(transaction_json),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: true
    }).done(function(response) { 
        if (response['success']) {
            printMessage('Added transaction successfuly.');            
        } else { 
            printMessage('Could not add transaction.');      
        }   
    }).fail(function() { 
        printMessage('Could not add transaction.');            
    })
}




