import {apiUrl} from "/frontend/js/utils.js";

async function clickAddResume(){
    const jwtTokenName = 'access_token';
        const token = getCookie(jwtTokenName);
        console.log(token)
        if(token){
            window.location.href=apiUrl+"/resumes/add"
        } else {
            window.location.href=apiUrl+'/login';
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
    }
}

 async function clickProfile(){
        const jwtTokenName = 'access_token';
        const token = getCookie(jwtTokenName);
        console.log(token)
        if(token){
            window.location.href=apiUrl+'/worker/profile';
        } else {
            window.location.href=apiUrl+'/login';
        }
}

window.clickAddResume = clickAddResume
window.clickProfile = clickProfile