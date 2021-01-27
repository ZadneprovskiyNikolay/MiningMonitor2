window.addEventListener('DOMContentLoaded', onload);

function onload() {
    loadTransactionsPromise()
    .then(fillTransactionsTable)
    .catch(function() {});      
}

function loadTransactionsPromise() {  
    return new Promise(function (resolve, reject) {
        $.getJSON('/transactions/transactions.json').done(function(data, textStatus, jqXHR) {             
            resolve(data);
        }).fail(function(jqxhr, textStatus, error) {
            reject(error);
        });
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
