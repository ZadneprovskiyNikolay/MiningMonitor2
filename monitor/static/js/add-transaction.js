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
    let data = formToJSON(form);
    if (!data) return;

    var mutation_params = createParamStringGraphql(data);
    var mutation = {
        query: 
        `mutation FirstMutation {
            createTransaction(transactionData: {${mutation_params}}) {    
                transaction {
                    amount
                    date
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