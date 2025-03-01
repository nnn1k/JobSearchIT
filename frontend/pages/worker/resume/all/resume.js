import {print_salary} from "/frontend/js/print_salary.js";
import {formatDateTime} from "/frontend/js/timefunc.js";
import {apiUrl, makeRequest} from "/frontend/js/utils.js";
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
    if (!getResponse) {
        hideLoadingIndicator(loadingIndicator)
    }
    const resumes = getResponse.user.resumes;
    const container = document.getElementById('resume-container');

    if (resumes.length === 0) {
        container.style.marginTop = '15%'
        const noResumesLabel = document.createElement('h2');
        noResumesLabel.textContent = `У вас еще нет резюме. Мы можете создать его `;

        const link = document.createElement('a');
        link.textContent = 'тут';
        link.href = '/resumes/add';
        link.classList.add('resume-link');

        noResumesLabel.appendChild(link); // добавляем ссылку в текст
        container.appendChild(noResumesLabel);
        hideLoadingIndicator(loadingIndicator);
        return;
    }

    resumes.forEach(resume => {
        const linkElement = document.createElement('a')
        linkElement.href = apiUrl + `/resumes/${resume.id}`
        linkElement.style.color = '#555'

        const resumeElement = document.createElement('div');
        resumeElement.classList.add('resume');

        const titleElement = document.createElement('h2');
        titleElement.textContent = resume.profession.title;

        const salaryElement = document.createElement('p');
        print_salary(salaryElement, resume.salary_first, resume.salary_second)

        const cityElement = document.createElement('p');
        cityElement.innerHTML = `<strong>Город:</strong> ${resume.city}`;

        const updatedAtElement = document.createElement('p')
        updatedAtElement.innerHTML = `Обновлено ${formatDateTime(resume.updated_at)}`

        const editLink = document.createElement('a');
        editLink.classList.add('red_button');
        editLink.style.width = '30%';
        editLink.style.color = '#f2f2f2'
        editLink.addEventListener('mouseover', function() {
            editLink.style.color = 'crimson'; // Цвет текста ссылки при наведении
        });
        editLink.addEventListener('mouseout', function() {
            editLink.style.color = '#f2f2f2'; // Цвет текста ссылки при наведении
        });
        editLink.style.height = '15%';
        editLink.textContent = "Редактировать";
        editLink.href = apiUrl + `/worker/resumes/${resume.id}/edit`; // Устанавливаем ссылку

        const statsLabel = document.createElement('p');
        statsLabel.textContent = 'Статистика:'
        const stastElement = document.createElement('div');
        stastElement.classList.add('stats');
        stastElement.textContent = `0 приглашений`

        resumeElement.appendChild(titleElement);
        resumeElement.appendChild(updatedAtElement);
        resumeElement.appendChild(statsLabel);
        resumeElement.appendChild(stastElement);
        resumeElement.appendChild(salaryElement);
        resumeElement.appendChild(cityElement);
        resumeElement.appendChild(editLink);

        linkElement.appendChild(resumeElement)


        container.appendChild(linkElement);
    });
    hideLoadingIndicator(loadingIndicator);
}
