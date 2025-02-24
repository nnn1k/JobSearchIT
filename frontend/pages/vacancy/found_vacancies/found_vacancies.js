import {apiUrl, makeRequest} from '/frontend/js/utils.js';
import {hideLoadingIndicator, showLoadingIndicator} from '/frontend/js/functions_for_loading.js'
import {print_salary} from "/frontend/js/print_salary.js";
import {formatDateTime} from "/frontend/js/timefunc.js";

document.addEventListener('DOMContentLoaded', function () {
    getVacancies()
})


async function getVacancies(){
    const currentUrl = window.location.href;
    const url = new URL(currentUrl);

    const profession = url.searchParams.get("profession");
    const city =  url.searchParams.get("city")
    const min_salary =  url.searchParams.get("min_salary")

    const searchParams = new URLSearchParams();
    if (profession){
        searchParams.append('profession', profession);
        document.getElementById('job-search').value = profession
    }
    if (city){
        searchParams.append('city', city);
        document.getElementById('city').value = city

    }
    if (min_salary){
        searchParams.append('min_salary', min_salary);
        document.getElementById('salary').value = min_salary
    }

    const loadingIndicator = showLoadingIndicator();
    const getResponse = await makeRequest({
        method: 'GET',
        url: `/api/vacancy/?${searchParams.toString()}`
    })
    console.log(getResponse)
    if (getResponse.length === 0){
        const container = document.getElementById('vacancies-container');
        container.innerHTML = '';
        const countVacancyElement = document.createElement('h2');
        const secondMessage = document.createElement('h3')
        if (profession) {
             countVacancyElement.textContent = `По запросу "${profession}" ничего не найдено`
        }
        else {
            countVacancyElement.textContent = `По вашему запросу ничего не найдено`
        }
        secondMessage.textContent = ('Попробуйте другие варианты поискового запроса или уберите фильтры')
        container.appendChild(countVacancyElement);
        container.appendChild(secondMessage)
        hideLoadingIndicator(loadingIndicator)
        return
    }
    renderVacancies(getResponse.vacancies, true, profession ,getResponse.length, )
    hideLoadingIndicator(loadingIndicator)
}

function renderVacancies(vacancies, can_update, name_vacancy, count_vacancy) {
    const container = document.getElementById('vacancies-container');
    container.innerHTML = '';

    const countVacancyElement = document.createElement('h2');

    if (name_vacancy){
        countVacancyElement.textContent = `${count_vacancy} вакансий "${name_vacancy}"`
        container.appendChild(countVacancyElement);
    }
    else{
        countVacancyElement.textContent = ` Найдено ${count_vacancy} вакансий`
        container.appendChild(countVacancyElement);
    }

    vacancies.forEach(vacancy => {
        const vacancyElement = document.createElement('div');
        vacancyElement.classList.add('vacancy');

        const linkElement = document.createElement('a');
        linkElement.href = `/vacancies/${vacancy.id}`;
        linkElement.style.textDecoration = 'none';

        const titleElement = document.createElement('h2');
        titleElement.textContent = vacancy.profession.title;

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


        // if (userType === 'worker' || !userType){
        //     const feedbackButton = document.createElement('button');
        //     feedbackButton.classList.add('red_button');
        //     feedbackButton.style.width = '30%';
        //     feedbackButton.textContent = "Откликнуться";
        //     vacancyElement.appendChild(feedbackButton);
        //     container.appendChild(vacancyElement);
        //     return;
        // }

        if (can_update) {
            const editButton = document.createElement('button');
            editButton.classList.add('red_button');
            editButton.style.width = '30%';
            editButton.textContent = "Откликнуться";
            editButton.onclick = () => {
                window.location.href = `/vacancies/${vacancy.id}/edit`;
            };
            vacancyElement.appendChild(editButton);
            container.appendChild(vacancyElement);
            return;
        }
        container.appendChild(vacancyElement);
    });
}


async function searchVacancy(){
    const profession = document.getElementById('job-search').value;
    const city = document.getElementById('city').value
    const min_salary = document.getElementById('salary').value
    const searchParams = new URLSearchParams();
    if (profession){
        searchParams.append('profession', profession);
    }
    if (city){
        searchParams.append('city', city);
    }
    if (min_salary){
        searchParams.append('min_salary', min_salary);
    }
    const searchUrl = apiUrl + `/vacancies/?${searchParams.toString()}`;

    window.location.href = searchUrl;
}


window.searchVacancy = searchVacancy