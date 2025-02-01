import {apiUrl} from "/frontend/js/utils.js";

async function clickAddVacancy(){

    const jwtTokenName = 'access_token';
        const token = getCookie(jwtTokenName);
        console.log(token)
        if(token){
            window.location.href=apiUrl+"/vacancies/add"
        } else {
            window.location.href=apiUrl+'/login';
        }
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

window.onload = function() {
    const jwtTokenName = 'access_token';
    const token = getCookie(jwtTokenName);
    if(!token){
      document.getElementById('choose_role').style.display = 'flex';
    }
}

 async function clickProfile(){
        const jwtTokenName = 'access_token';
        const token = getCookie(jwtTokenName);
        console.log(token)
        if(token){
            window.location.href=apiUrl+'/employer/profile';
        } else {
            window.location.href=apiUrl+'/login';
        }
}

window.clickAddVacancy = clickAddVacancy
window.clickProfile = clickProfile