import {apiUrl, makeRequest} from "/frontend/js/utils.js";

document.addEventListener('DOMContentLoaded', function () {
    get_company()
    const first_button = document.getElementById('switch_description')
    showForm('desc_form', first_button)
})

async function get_company() {
    const company_id = location.pathname.split('/')[2]
    const getResponse = await makeRequest({
        method: 'GET',
        url: `/api/companies/${company_id}`
    })
    console.log(getResponse)
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
        width: 600,
        height: 500,
        fontsize: 50,
        whiteSpace: "pre-wrap"
    });

    tinymce.get('company_description_update').setContent(getResponse.company.description)
    document.getElementById('company_description_update').value = getResponse.company.description;
    renderVacancies(getResponse.vacancies)
}

async function update_company() {
    const company_id = location.pathname.split('/')[2]
    const description = tinymce.get('company_description_update').getContent()
    const putResponse = await makeRequest({
        method: 'PUT',
        url: `/api/companies/${company_id}`,
        data: {
            description
        }
    })

    console.log(putResponse)
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


function renderVacancies(vacancies) {
    const container = document.getElementById('vacancies-container');
    container.innerHTML = '';

    vacancies.forEach(vacancy => {
        const vacancyElement = document.createElement('div');
        vacancyElement.classList.add('vacancy');

        const titleElement = document.createElement('h2');

        const titleLink = document.createElement('a');
        titleLink.href = `/vacancies/${vacancy.id}`;
        titleLink.textContent = vacancy.title;
        titleLink.setAttribute('target', '_blank')
        titleElement.appendChild(titleLink);
        const salaryElement = document.createElement('p');
        const salary_first = vacancy.salary_first;
        const salary_second = vacancy.salary_second;
        if (!salary_first && !salary_second)
            salaryElement.innerHTML = ''
        else
            salaryElement.innerHTML += `<strong>Зарплата (руб.):</strong>`
        if (salary_first)
            salaryElement.innerHTML += ` от ${salary_first}`
        if (salary_second)
            salaryElement.innerHTML += ` до ${salary_second}`

        const cityElement = document.createElement('p');
        cityElement.innerHTML = `<strong>Город:</strong> ${vacancy.city}`;

        vacancyElement.appendChild(titleElement);
        vacancyElement.appendChild(salaryElement);
        vacancyElement.appendChild(cityElement);

        container.appendChild(vacancyElement);
    });
}

window.update_company = update_company
window.showForm = showForm