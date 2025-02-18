import {makeRequest} from "/frontend/js/utils.js";
import {hideLoadingIndicator, showLoadingIndicator} from '/frontend/js/functions_for_loading.js'
import {print_salary} from "/frontend/js/print_salary.js";
import {createTrashBtnVacancy} from "/frontend/js/create_trash_can.js";

async function get_vacancy() {
    const vacancyId = location.pathname.split('/')[2]
    const vacancyContainer = document.getElementById('vacancy-container')
    vacancyContainer.style.display = 'none'
    const loadingIndicator = showLoadingIndicator();
    const getResponse = await makeRequest({
        method: 'GET',
        url: `/api/vacancy/${vacancyId}`
    })
    console.log(getResponse)
    if (getResponse) {
        const vacancy = getResponse.vacancy;
        const companyName = getResponse.vacancy.company.name;
        const skills = getResponse.vacancy.skills;
        const deleteElement = document.getElementById('btn_delete')
        if (getResponse.can_update) {
            deleteElement.style.display = 'flex';
            const trashBtn = createTrashBtnVacancy(vacancy);
            deleteElement.appendChild(trashBtn);
        }
        document.getElementById('title_vacancy').innerHTML = vacancy.title;
        document.getElementById('name_company').innerHTML = companyName;
        document.getElementById('city_vacancy').innerHTML = vacancy.city;
        const salaryElement = document.getElementById('salary_vacancy')
        print_salary(salaryElement, vacancy.salary_first, vacancy.salary_second)
        document.getElementById('description_vacancy').innerHTML = vacancy.description;
        const link_company = document.getElementById("link_company");
        link_company.href = `/companies/${vacancy.company_id}`;
        const skillsList = document.getElementById('skillsList');
        console.log(skills)
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
        hideLoadingIndicator(loadingIndicator);
        vacancyContainer.style.display = 'block'

    }
}

document.addEventListener('DOMContentLoaded', function () {
    get_vacancy()
})