import {apiUrl, makeRequest} from '../../../js/utils.js';

async function auth() {
    const email = document.getElementById("login").value
    const password = document.getElementById("password").value
    const  confirm_password = document.getElementById("confirm_password").value
    const response = await makeRequest({
        method: 'POST',
        url: '/api/auth/workers/register',
        data: {
            email,
            password,
            confirm_password
        }
    })
    console.log('response:', response)
}
window.auth = auth;