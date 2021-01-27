document.addEventListener("DOMContentLoaded", function() {
    let signin_button = document.getElementById("signin");    
    if (signin_button) {
        signin_button.onclick = signinFun;
    }
    
});
 
function signinFun(e) { 
    // Don't use jquery $.ajax because I can't make it resolve 302 resoponse
    e.preventDefault();        

    let form = document.getElementById('form');
    let user = formToJSON(form);
    
    // send login and password to web server            
    let xhr = new XMLHttpRequest();
    let url = window.location.href;
    xhr.open("POST", url, true);
    xhr.onload = function() {        
        switch (xhr.status) {
            case 403:
                printMessage('incorrect username or password');
                break;
            case 200:        
                window.location.href = xhr.responseURL;
        }
    }
    xhr.setRequestHeader("Content-Type", "application/json");    
    let data = JSON.stringify(user);
    xhr.send(data);    

}


