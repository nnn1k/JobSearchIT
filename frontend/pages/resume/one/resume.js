import {makeRequest} from "/frontend/js/utils.js";
import {print_salary} from "/frontend/js/print_salary.js";


document.addEventListener('DOMContentLoaded', function (){
    get_resume()
})

async function get_resume(){
    const resume_id = location.pathname.split('/')[2]
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
    if (getResponse.can_update){
        const deleteBtn = document.getElementById('btn_delete')
        deleteBtn.style.display = 'flex'
        deleteBtn.onclick = () => {
            window.location.href = `/worker/resumes/${resume.id}/edit`
        }
    }
}