import {makeRequest} from "/frontend/js/utils.js";
import {displaySelectedSkills} from "/frontend/js/skills.js";

tinymce.init({
    menubar: false,
    statusbar: false,
    display: "flex",
    selector: '#input_for_description_vacancy',
    width: 600,
    height: 500,
    fontsize: 50,
    whiteSpace: "pre-wrap"
});
document.addEventListener('DOMContentLoaded', function (){
    get_resume()
})

async function get_resume(){
    const resume_id = location.pathname.split('/')[3]
    const getResponse = await makeRequest({
        method: 'GET',
        url: `/api/workers/resumes/${resume_id}`
    })
    console.log(getResponse)
    const resume= getResponse.resume
    document.getElementById('input_for_title_vacancy').value = resume.title
    document.getElementById('input_for_city_vacancy').value = resume.city
    tinymce.get('input_for_description_vacancy').setContent(resume.description)
    document.getElementById('input_for_first_salary').value = resume.salary_first
    document.getElementById('input_for_second_salary').value = resume.salary_second
    displaySelectedSkills(getResponse.skills, true)
}