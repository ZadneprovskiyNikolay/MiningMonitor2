transaction_fields = ['date', 'amount'];

window.addEventListener('DOMContentLoaded', onload);

function onload() {
    loadTransactionsPromise()
    .then(fillTransactionsTable)
    .catch(function() {});      
}

function loadTransactionsPromise() {      
    return new Promise(function(resolve, reject) { 
        var query = { query: `
            query {
                transactions {    
                    ${transaction_fields.join('\n')}
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
            rows = [];   
            for (data of r['data']['transactions']) {
                new_row = [];
                for (field of transaction_fields) { 
                    new_row.push(data[field]);
                }
                rows.push(new_row);
            }
            resolve(rows); 
        })        
        .catch(error => { 
            console.error('Error loading transactions: ' + error);
            reject();
        })   
        return;     
    })        
}    

function fillTransactionsTable(transactions) { 
    if (transactions.length == 0) {
        return;           
    }    
    var tableElement = document.getElementById('transactions-table');        

    generateTransactionsTableHead(tableElement);
    generateTableBody(tableElement, transactions);
}

function generateTransactionsTableHead(table, rowId='table-header') {    
    var header = null
    header = ['date', 'amount']
    
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

function generateTableBody(table, transactions) {    
    // add rows to table
    var body = table.create
    for (transaction of transactions) {   
        var row = table.insertRow();        
        for (value of transaction) {
            var cell = row.insertCell();
            var text = document.createTextNode(value);
            cell.appendChild(text);
        }
    }
}
