import {apiUrl, makeRequest} from '/frontend/js/utils.js';
import {hideLoadingIndicator, showLoadingIndicator} from '/frontend/js/functions_for_loading.js'

async function signup_employer() {
    const email = document.getElementById("login").value
    const password = document.getElementById("password").value
    const confirm_password = document.getElementById("confirm_password").value
    const regBtn = document.getElementById('reg_btn')
    regBtn.disabled = true
    const loadingIndicator = showLoadingIndicator();
    const postResponse = await makeRequest({
        method: 'POST',
        url: '/api/auth/employers/register',
        data: {
            email,
            password,
            confirm_password
        }
    })
    if (postResponse) {
        const getResponse = await makeRequest({
                method: 'GET',
                url: '/api/auth/employers/code',
            }
        )
        hideLoadingIndicator(loadingIndicator);
        regBtn.disabled = false

        const container1 = document.getElementById('container_worker');
        const container2 = document.getElementById('container_check_code');
        container1.style.display = 'none';
        container2.style.display = 'flex';
        container2.style.flexDirection = 'column';
        container2.style.justifyContent = 'center';
        container2.style.alignItems = 'center';
        container2.style.width = '350px';
        container2.style.gap = '30px';
    }
}


async function check_code() {
    const code = document.getElementById("code").value
    const checkBtn = document.getElementById('check_btn')
    checkBtn.disabled = true
    const loadingIndicator = showLoadingIndicator();
    const postResponse = await makeRequest({
        method: 'POST',
        url: '/api/auth/employers/code',
        data: {
            code
        }
    })
    if (postResponse) {
        hideLoadingIndicator(loadingIndicator);
        checkBtn.disabled = false
        window.location.href = apiUrl + "/signup/employer/profile"
    }
}

window.check_code = check_code;
window.signup_employer = signup_employer;

