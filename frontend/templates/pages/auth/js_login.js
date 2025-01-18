import {apiUrl, makeRequest} from '../../../js/utils.js';

$(document).ready(function() {
    $("#switchLoginForm_1").click(function() {
        $("#container_worker").toggle();
        $("#container_employer").toggle();
    });
    $("#switchLoginForm_2").click(function() {
        $("#container_worker").toggle();
        $("#container_employer").toggle();
    });
});

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
}
window.login_worker = login_worker;