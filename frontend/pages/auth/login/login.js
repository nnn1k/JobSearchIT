import {apiUrl, makeRequest} from '/frontend/js/utils.js';

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
    if (postResponse) {
        localStorage.setItem('user_type', 'worker');
        window.location.href = apiUrl + "/worker/profile"
    }
}

async function login_employer_form() {
    const email = document.getElementById('login_employer').value
    const password = document.getElementById('password_employer').value
    const postResponse = await makeRequest({
        method: 'POST',
        url: '/api/auth/employers/login',
        data: {
            email,
            password
        }
    })
    if (postResponse) {
        localStorage.setItem('user_type', 'employer');
        window.location.href = apiUrl + "/employer/profile"
    }
}

window.login_worker = login_worker;
window.login_employer_form = login_employer_form;


$(document).ready(function () {
    $("#switchLoginForm_1").click(function () {
        $("#container_worker").toggle();
        $("#container_employer").toggle();
    });
    $("#switchLoginForm_2").click(function () {
        $("#container_worker").toggle();
        $("#container_employer").toggle();
    });
});

