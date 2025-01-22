import {apiUrl, makeRequest} from '../../../js/utils.js';

async function login_worker() {
    const email = document.getElementById("login").value
    const password = document.getElementById("password").value
    const postResponse = await makeRequest({
        method: 'POST',
        url: '/api/auth/workers/login',
        data: {
            email,
            password
        }
    })
    if (postResponse){
        window.location.href=apiUrl+"/worker/profile"
    }
}

async function login_employer(){
    const email = document.getElementById('login_employer')
    const password = document.getElementById('password_employer')
    const postResponse = await makeRequest({
        method: 'POST',
        url: '/api/auth/employers/login',
        data: {
            email,
            password
        }
    })
    if (postResponse){
        window.location.href=apiUrl+"/employer/profile"
    }
}

window.login_worker = login_worker;



$(document).ready(function() {
    $("#switchLoginForm_1").click(function() {
        $("#container_worker").toggle(1000);
        $("#container_employer").toggle(1000);
    });
    $("#switchLoginForm_2").click(function() {
        $("#container_worker").toggle(1000);
        $("#container_employer").toggle(1000);
    });
});

