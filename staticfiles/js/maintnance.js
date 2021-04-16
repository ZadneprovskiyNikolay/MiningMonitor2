window.addEventListener('DOMContentLoaded', function() {
    $("#submit").click(function(e) {
        e.preventDefault();
        submitFun();  
        clearInput(['number-input']);
    });
})

function submitFun() {
    let form = document.getElementById('form');        
    let data = formToJSON(form);
    if (!data) return;

    // Submit change
    var mutation_params = createParamStringGraphql(data);
    var mutation = {
        query:  
        `mutation FirstMutation {
            setPowerCost(powerCost: {${mutation_params}}) {    
                powerCost {
                    startDate
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

function getChangeValue() { 
    return $('#maintenance-selector').val();
}