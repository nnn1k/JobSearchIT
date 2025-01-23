import {apiUrl, makeRequest} from '/frontend/js/utils.js';

async function signup_employer() {
    const email = document.getElementById("login").value
    const password = document.getElementById("password").value
    const confirm_password = document.getElementById("confirm_password").value
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
        console.log(getResponse)
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
    console.log(code)
    const postResponse = await makeRequest({
        method: 'POST',
        url: '/api/auth/employers/code',
        data: {
            code
        }
    })
    if (postResponse) {
        window.location.href = apiUrl + "/signup/employer/profile"
    }
}

window.check_code = check_code;
window.signup_employer = signup_employer;

