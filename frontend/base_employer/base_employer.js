import {apiUrl, makeRequest} from "/frontend/js/utils.js";

async function clickAddVacancy() {

    const jwtTokenName = 'access_token';
    const token = getCookie(jwtTokenName);
    console.log(token)
    if (token) {
        window.location.href = apiUrl + "/vacancies/add"
    } else {
        window.location.href = apiUrl + '/login';
    }
}

async function logout() {
    const logoutResponse = await makeRequest({
        method: 'POST',
        url: '/api/auth/logout/'
    })
    if (logoutResponse) {
        location.reload(true)
    }
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

window.onload = function () {
    const jwtTokenName = 'access_token';
    const token = getCookie(jwtTokenName);
    if (!token) {
        document.getElementById('choose_role').style.display = 'flex';
        const loginBtn = document.getElementById('login-btn')
        loginBtn.style.display = 'block'
        loginBtn.addEventListener('click', function () {
            window.location.href = apiUrl + '/login';
        })
    }
    else {
        document.getElementById('account-btn').style.display = 'block'
    }
}

async function clickProfile() {
    const jwtTokenName = 'access_token';
    const token = getCookie(jwtTokenName);
    console.log(token)
    if (token) {
        window.location.href = apiUrl + '/employer/profile';
    } else {
        window.location.href = apiUrl + '/login';
    }
}

const profileBtn = document.getElementById('pic_profile');
const dropdownMenu = document.getElementById('dropdownMenu');

profileBtn.addEventListener('click', function () {
    event.stopPropagation(); // Предотвращаем всплытие события
    dropdownMenu.style.display = dropdownMenu.style.display === 'none' || dropdownMenu.style.display === '' ? 'block' : 'none';

});

window.onclick = function (event) {
    if (!event.target.matches('#pic_profile')) {
        const dropdown = document.getElementById("dropdownMenu");
        if (dropdown.style.display === "block") {
            dropdown.style.display = "none";
        }
    }
}

dropdownMenu.addEventListener('click', function (event) {
    event.stopPropagation(); // Предотвращаем скрытие меню при клике внутри
});


window.clickAddVacancy = clickAddVacancy
window.clickProfile = clickProfile
window.logout = logout
