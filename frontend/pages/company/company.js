import {apiUrl, makeRequest} from "/frontend/js/utils.js";
import {print_salary} from "/frontend/js/print_salary.js";
import {formatDateTime} from "/frontend/js/timefunc.js";
import {hideLoadingIndicator, showLoadingIndicator} from '/frontend/js/functions_for_loading.js'

document.addEventListener('DOMContentLoaded', function () {
    get_company()
    const first_button = document.getElementById('switch_description')
    showForm('desc_form', first_button)
})

async function get_company() {
    const loadingIndicator = showLoadingIndicator();
    const company_id = location.pathname.split('/')[2]
    const getResponse = await makeRequest({
        method: 'GET',
        url: `/api/companies/${company_id}`
    })
    const company = getResponse.company;
    document.getElementById('company_name').innerHTML = company.name;
    document.getElementById('company_description').innerHTML = company.description;
    if (getResponse.can_update) {
        document.getElementById('can_update').style.display = 'block';
    }
    tinymce.init({
        menubar: false,
        statusbar: false,
        display: "flex",
        selector: '#company_description_update',
        width: 1000,
        height: 600,
        fontsize: 50,
        whiteSpace: "pre-wrap"
    });
    hideLoadingIndicator(loadingIndicator);
    tinymce.get('company_description_update').setContent(getResponse.company.description)
    document.getElementById('company_description_update').value = getResponse.company.description;
    renderVacancies(getResponse.company.vacancies, getResponse.can_update)

}

async function update_company() {
    const loadingIndicator = showLoadingIndicator();
    const company_id = location.pathname.split('/')[2]
    const description = tinymce.get('company_description_update').getContent()
    const putResponse = await makeRequest({
        method: 'PUT',
        url: `/api/companies/${company_id}`,
        data: {
            description
        }
    })
    hideLoadingIndicator(loadingIndicator);
    location.reload(true)
}


function showForm(formId, button) {
    const forms = document.querySelectorAll('.form_container')
    forms.forEach(form => {
        form.style.display = 'none';
    })
    const selectedForm = document.getElementById(formId)
    selectedForm.style.display = 'flex';

    const buttons = document.querySelectorAll('.btn')
    buttons.forEach(btn => {
        btn.classList.remove('active')
    })
    button.classList.add('active');
}


function renderVacancies(vacancies, can_update) {
    const container = document.getElementById('vacancies-container');
    container.innerHTML = '';

    vacancies.forEach(vacancy => {
        const vacancyElement = document.createElement('div');
        vacancyElement.classList.add('vacancy');

        const linkElement = document.createElement('a');
        linkElement.href = `/vacancies/${vacancy.id}`;
        linkElement.style.textDecoration = 'none';

        const titleElement = document.createElement('h2');
        titleElement.textContent = vacancy.title;

        const salaryElement = document.createElement('p');
        print_salary(salaryElement, vacancy.salary_first, vacancy.salary_second)

        const cityElement = document.createElement('p');
        cityElement.innerHTML = `<strong>Город:</strong> ${vacancy.city}`;

        const updatedAtElement = document.createElement('p')
        updatedAtElement.innerHTML = `Обновлено ${formatDateTime(vacancy.updated_at)}`

        const statsLabel = document.createElement('p');
        statsLabel.textContent = 'Статистика:'
        const stastElement = document.createElement('div');
        stastElement.classList.add('stats');
        stastElement.textContent = `0 откликов`

        linkElement.appendChild(titleElement);
        linkElement.appendChild(updatedAtElement);
        linkElement.appendChild(statsLabel);
        linkElement.appendChild(stastElement);
        linkElement.appendChild(salaryElement);
        linkElement.appendChild(cityElement);
        vacancyElement.appendChild(linkElement);


        if (can_update) {
            const editButton = document.createElement('button');
            editButton.classList.add('red_button');
            editButton.style.width = '30%';
            editButton.textContent = "Редактировать";
            editButton.onclick = () => {
                window.location.href = `/employer/vacancies/${vacancy.id}/edit`;
            };
            vacancyElement.appendChild(editButton);
            container.appendChild(vacancyElement);
        }
    });
}

window.update_company = update_company
window.showForm = showForm