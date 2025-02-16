import {makeRequest} from "/frontend/js/utils.js";
import {hideLoadingIndicator, showLoadingIndicator} from '/frontend/js/functions_for_loading.js'

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
    const loadingIndicator = showLoadingIndicator();
    const getResponse = await makeRequest({
        method: 'GET',
        url: `/api/workers/resumes/${resume_id}`
    })
    console.log(getResponse)
    hideLoadingIndicator(loadingIndicator);
    const resume= getResponse.resume
    const skills = getResponse.resume.worker.skills
    document.getElementById('input_for_title_vacancy').value = resume.title
    document.getElementById('input_for_city_vacancy').value = resume.city
    tinymce.get('input_for_description_vacancy').setContent(resume.description)
    document.getElementById('input_for_first_salary').value = resume.salary_first
    document.getElementById('input_for_second_salary').value = resume.salary_second
    const displaySkills = () => {
            const skillsDisplay = document.getElementById('skillsList');
            skillsDisplay.innerHTML = '';

            if (skills.length === 0) {
                document.getElementById('form-group').style.display = 'none'
                return;
            }
            skills.forEach(skill => {
                const skillTag = document.createElement('div');
                skillTag.className = 'skill-tag';
                console.log(skill.name)
                skillTag.textContent = skill.name;
                skillsDisplay.appendChild(skillTag);
            });
            };
        displaySkills();
}