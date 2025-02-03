import {makeRequest} from "/frontend/js/utils.js";
import {print_salary} from "/frontend/js/print_salary.js";

document.addEventListener('DOMContentLoaded', function (){
    get_resume()
})

async function get_resume(){
    const resume_id = location.pathname.split('/')[3]
    const getResponse = await makeRequest({
        method: 'GET',
        url: `/api/workers/resumes/${resume_id}`
    })
    console.log(getResponse.resume)
    const resume= getResponse.resume
    document.getElementById('resume_title').innerHTML = resume.title
    const salaryElement = document.getElementById('salary')
    print_salary(salaryElement, resume.salary_first, resume.salary_second)
    document.getElementById('city').innerHTML = resume.city
    document.getElementById('description').innerHTML = resume.description

}