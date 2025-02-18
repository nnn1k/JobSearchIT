import {print_salary} from "/frontend/js/print_salary.js";
import {formatDateTime} from "/frontend/js/timefunc.js";
import {makeRequest} from "/frontend/js/utils.js";
import {hideLoadingIndicator, showLoadingIndicator} from '/frontend/js/functions_for_loading.js'

document.addEventListener('DOMContentLoaded', function () {
    get_resumes()
})

async function get_resumes() {
    const loadingIndicator = showLoadingIndicator();
    const getResponse = await makeRequest({
        method: 'GET',
        url: '/api/workers/me/'
    })
    console.log(getResponse)
    const resumes = getResponse.user.resumes;
    const container = document.getElementById('resume-container');

    resumes.forEach(resume => {
        const resumeElement = document.createElement('div');
        resumeElement.classList.add('resume');

        const titleElement = document.createElement('h2');
        titleElement.textContent = resume.title;

        const salaryElement = document.createElement('p');
        print_salary(salaryElement, resume.salary_first, resume.salary_second)

        const cityElement = document.createElement('p');
        cityElement.innerHTML = `<strong>Город:</strong> ${resume.city}`;

        const updatedAtElement = document.createElement('p')
        updatedAtElement.innerHTML = `Обновлено ${formatDateTime(resume.updated_at)}`

        const editButton = document.createElement('button');
        editButton.classList.add('red_button');
        editButton.style.width = '40%';
        editButton.style.height = '25%';
        editButton.style.marginLeft = '60%';
        editButton.textContent = "Редактировать";

        editButton.onclick = () => {
            window.location.href = `/worker/resumes/${resume.id}/edit`;
        };

        resumeElement.appendChild(titleElement);
        resumeElement.appendChild(updatedAtElement)
        resumeElement.appendChild(salaryElement);
        resumeElement.appendChild(cityElement);
        resumeElement.appendChild(editButton);

        container.appendChild(resumeElement);
    });
    hideLoadingIndicator(loadingIndicator);
}
