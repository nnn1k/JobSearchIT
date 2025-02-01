import {apiUrl, makeRequest} from "/frontend/js/utils.js";
import {displaySelectedSkills, createSkillButtons, getSelectedSkills} from '/frontend/js/skills.js'

document.addEventListener('DOMContentLoaded', function (){
    getSkills()
})

async function getSkills(){
    const getResponse = await makeRequest({
        method: 'GET',
        url: '/api/skills/worker/me'
    })
    const available_skills = getResponse.available_skills
    const worker_skills = getResponse.worker_skills
    createSkillButtons(available_skills)
    displaySelectedSkills(worker_skills)
}

async function postResume(){
    const title = document.getElementById('title').value
    const description = document.getElementById('description').value
    const salary_first = Number(document.getElementById('salary_first').value)
    const salary_second = Number(document.getElementById('salary_second').value)
    const city = document.getElementById('city').value
    const skills = getSelectedSkills()
    const postResponse = await makeRequest({
        method: 'POST',
        url: '/api/resumes/',
        data: {
            title,
            description,
            salary_first,
            salary_second,
            city,
            skills
        }
    })
    if (postResponse.status) {
        alert('Резюме добавлено')
        window.location.href = apiUrl + '/worker/profile'
    }
}

function submitResume(event) {
    event.preventDefault(); // Предотвращаем обновление страницы
    postResume()
}



window.submitResume = submitResume
