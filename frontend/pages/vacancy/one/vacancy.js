import {apiUrl, makeRequest} from "/frontend/js/utils.js";
import {hideLoadingIndicator, showLoadingIndicator} from '/frontend/js/functions_for_loading.js'
import {print_salary} from "/frontend/js/print_salary.js";
import {createTrashBtnVacancy} from "/frontend/js/create_trash_can.js";
import {createModal} from "/frontend/js/modal_window.js";

var resumes

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}


async function getMyResumes() {
    const userType = getCookie('user_type')
    if (!userType || userType === 'employer') {
        return
    }
    const getMyResumes = await makeRequest({
        method: 'GET',
        url: '/api/resumes/me'
    })
    resumes = getMyResumes.resumes
}


async function getVacancy() {
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
        const flexBtn = document.getElementById('otlik_btn')
        const deleteElement = document.getElementById('btn_delete')
        if (getResponse.can_update) {
            deleteElement.style.display = 'flex';
            const trashBtn = createTrashBtnVacancy(vacancy);
            deleteElement.appendChild(trashBtn);
        }
        document.getElementById('title_vacancy').innerHTML = vacancy.profession.title
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
                skillTag.textContent = skill.name;
                skillsDisplay.appendChild(skillTag);
            });
            };
        if (getResponse.can_update){
            flexBtn.textContent = 'Редактировать'
            flexBtn.onclick = () => {
                window.location.href = `/vacancies/${vacancy.id}/edit`;
            };
        }

        const userType = getCookie('user_type')

        if (userType === 'worker' || !userType){
            flexBtn.textContent = 'Откликнуться'
            flexBtn.onclick = function () {
                if (!userType) {
                    window.location.href = apiUrl + '/login';
                    return
                }

                createModal('Выберите резюме для отклика', resumes, vacancy.id);
            };
        }

        if (userType === 'employer' && !getResponse.can_update){
            flexBtn.style.display = 'none'
        }
        displaySkills();
        hideLoadingIndicator(loadingIndicator);
        vacancyContainer.style.display = 'block'
    }
}

document.addEventListener('DOMContentLoaded', function () {
    getVacancy()
    getMyResumes()
})