import {apiUrl, makeRequest} from '/frontend/js/utils.js';
import {createSkillButtons, displaySelectedSkills, getSelectedSkills} from "/frontend/js/skills.js";

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
document.addEventListener('DOMContentLoaded', () => {
    getSkills()
})

async function getSkills(){
    const getResponse = await makeRequest({
        method: 'GET',
        url: '/api/skills/'
    })
    const skills = getResponse.skills
    createSkillButtons(skills)
}

async function post_vacancy() {
    const title = document.getElementById('input_for_title_vacancy').value
    const description = tinymce.get('input_for_description_vacancy').getContent()
    const salary_first = Number(document.getElementById('input_for_first_salary').value)
    const salary_second = Number(document.getElementById('input_for_second_salary').value)
    const city = document.getElementById('input_for_city_vacancy').value
    const skills = getSelectedSkills()
    if (!title){
        alert('Не все данные заполнены')
        return
    }

    const postResponse = await makeRequest({
        method: 'POST',
        url: '/api/vacancy',
        data: {
            title,
            description,
            salary_first,
            salary_second,
            city,
            skills
        }
    })
    if (postResponse) {
        window.location.href = apiUrl + "/vacancies/add"
        alert('Вакансия опубликована');
    }
}

window.post_vacancy = post_vacancy