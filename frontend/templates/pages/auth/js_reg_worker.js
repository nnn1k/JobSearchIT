import {apiUrl, makeRequest} from '../../../js/utils.js';

async function auth() {
    const login = document.getElementById("login").value
    const password = document.getElementById("password").value
    const  confirm_password = document.getElementById(" confirm_password").value
    console.log(login)
    console.log(password)
    console.log(confirm_password)
    const response = await makeRequest({
        method: 'POST',
        url: '/api/auth/workers/register',
        data: {
            login,
            password,
            confirm_password
        }
    })
    console.log('response:', response)
}
window.auth = auth;