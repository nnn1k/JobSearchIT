import {apiUrl, makeRequest} from '/frontend/js/utils.js';
import {hideLoadingIndicator, showLoadingIndicator} from '/frontend/js/functions_for_loading.js'


async function login_worker() {
    const email = document.getElementById("login").value
    const password = document.getElementById("password").value
    const loginBtn = document.getElementById('login_btn')
    loginBtn.disabled = true
    const loadingIndicator = showLoadingIndicator();
    const postResponse = await makeRequest({
        method: 'POST',
        url: '/api/auth/workers/login',
        data: {
            email,
            password
        }
    })
    if (postResponse) {
        hideLoadingIndicator(loadingIndicator);
        loginBtn.disabled = false
        window.location.href = apiUrl + "/worker/profile"
    }
    hideLoadingIndicator(loadingIndicator);
    loginBtn.disabled = false
}

async function login_employer_form() {
    const email = document.getElementById('login_employer').value
    const password = document.getElementById('password_employer').value
    const loginBtn = document.getElementById('login_btn_2')
    loginBtn.disabled = true
    const loadingIndicator = showLoadingIndicator();
    const postResponse = await makeRequest({
        method: 'POST',
        url: '/api/auth/employers/login',
        data: {
            email,
            password
        }
    })
    if (postResponse) {
        hideLoadingIndicator(loadingIndicator);
        loginBtn.disabled = false
        window.location.href = apiUrl + "/employer/profile"
    }
    hideLoadingIndicator(loadingIndicator);
    loginBtn.disabled = false
}

window.login_worker = login_worker;
window.login_employer_form = login_employer_form;


$(document).ready(function () {
    $("#switchLoginForm_1").click(function () {
        $("#container_worker").toggle(0);
        $("#container_employer").fadeToggle(1000);
        $('#switchLoginForm_2').prop('disabled', true);
        setTimeout(() => {
            $('#switchLoginForm_2').prop('disabled', false);
        }, 1100);
    });
    $("#switchLoginForm_2").click(function () {
        $("#container_worker").fadeToggle(1000);
        $("#container_employer").toggle(0);
        $('#switchLoginForm_1').prop('disabled', true);
        setTimeout(() => {
            $('#switchLoginForm_1').prop('disabled', false);
        }, 1100);
    });
});

