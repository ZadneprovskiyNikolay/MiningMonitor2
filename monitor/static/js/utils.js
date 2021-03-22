function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function setCsrfToken() {
    var csrftoken = Cookies.get('csrftoken');  
    
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}

function isEmptyOrSpaces(str) {
    return str === null || str.match(/^ *$/) !== null;
}

const formToJSON = elements => [].reduce.call(elements, (data, element) => {
    if (!isEmptyOrSpaces(element.name)) {
        if (element.type && element.type === 'checkbox') {
            data[element.name] = element.checked;
         } else {
             data[element.name] = element.value;    
         }
    }
    return data;
}, {});

function printMessage(msg) {    
    document.getElementById('message').innerHTML = msg;
}

function clearInput(inputIds) { 
    // Wrap inputIds in array 
    if (typeof(inputIds) == 'string') { 
        inputIds = [inputIds];
    }

    for (id of inputIds) { 
        el = document.getElementById(id);
        if (el) {
            if (el.getAttribute('type') == 'checkbox') {
                el.checked = false;
            } else {
                el.value = "";
            }
        }
    }
}