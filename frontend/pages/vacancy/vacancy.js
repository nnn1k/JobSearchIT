import {apiUrl, makeRequest} from "/frontend/js/utils.js";
import {hideLoadingIndicator, showLoadingIndicator} from '/frontend/js/functions_for_loading.js'

async function get_vacancy(){
    const vacancyId = location.pathname.split('/')[2]
    const vacancyContainer = document.getElementById('vacancy-container')
    vacancyContainer.style.display = 'none'
    const loadingIndicator = showLoadingIndicator();
    const getResponse = await makeRequest({
        method: 'GET',
        url: `/api/vacancy/${vacancyId}`
    })
    if (getResponse) {
        const vacancy = getResponse.vacancy;
        const companyName = getResponse.company_name
        console.log(getResponse)
        document.getElementById('title_vacancy').innerHTML = vacancy.title;
        document.getElementById('name_company').innerHTML = companyName;
        document.getElementById('city_vacancy').innerHTML = vacancy.city;
        const salaryElement = document.getElementById('salary_vacancy')
        salaryElement.innerHTML = `<strong>Зарплата:</strong>`;
        if (!vacancy.salary_first && !vacancy.salary_second)
            salaryElement.innerHTML += ' Не указана';
        else {
            if (vacancy.salary_first)
                salaryElement.innerHTML += ` от ${vacancy.salary_first}`;
            if (vacancy.salary_second)
                salaryElement.innerHTML += ` до ${vacancy.salary_second}`;
            salaryElement.innerHTML += ' руб.'
        }
        document.getElementById('description_vacancy').innerHTML = vacancy.description;
        hideLoadingIndicator(loadingIndicator);
        vacancyContainer.style.display = 'block'
    }


}


document.addEventListener('DOMContentLoaded', function () {
    get_vacancy()
})