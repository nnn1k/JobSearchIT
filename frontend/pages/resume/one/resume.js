import {makeRequest} from "/frontend/js/utils.js";
import {print_salary} from "/frontend/js/print_salary.js";
import {displaySelectedSkills} from "/frontend/js/skills.js";
import {hideLoadingIndicator, showLoadingIndicator} from '/frontend/js/functions_for_loading.js'


document.addEventListener('DOMContentLoaded', function (){
    get_resume()
})

async function get_resume(){
    const resume_id = location.pathname.split('/')[2]
    const loadingIndicator = showLoadingIndicator();
    const mainScreen = document.getElementById('vacancy-container')
    mainScreen.style.display = 'none'
    const getResponse = await makeRequest({
        method: 'GET',
        url: `/api/workers/resumes/${resume_id}`
    })
    console.log(getResponse)
    const resume= getResponse.resume
    document.getElementById('title').innerHTML += resume.title
    document.title = resume.title
    const salaryElement = document.getElementById('salary')
    print_salary(salaryElement, resume.salary_first, resume.salary_second)
    document.getElementById('city').innerHTML += resume.city
    document.getElementById('description').innerHTML = resume.description
    displaySelectedSkills(getResponse.skills, true)
    if (getResponse.can_update){
        hideLoadingIndicator(loadingIndicator);
        const editBtn = document.getElementById('edit_btn')
        const feedbackBtn = document.getElementById('feedback')
        feedbackBtn.style.display = 'none'
        editBtn.style.display = 'block'
        editBtn.style.width = '35%'
        editBtn.onclick = () => {
            window.location.href = `/worker/resumes/${resume.id}/edit`

        }
    }
    mainScreen.style.display = 'block'
    hideLoadingIndicator(loadingIndicator);
}