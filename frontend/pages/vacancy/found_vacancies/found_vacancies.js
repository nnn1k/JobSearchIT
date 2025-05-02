import {apiUrl, makeRequest} from '/frontend/js/utils.js';
import {hideLoadingIndicator, showLoadingIndicator} from '/frontend/js/functions_for_loading.js'
import {print_salary} from "/frontend/js/print_salary.js";
import {formatDateTime} from "/frontend/js/timefunc.js";
import {createModal} from "/frontend/js/modal_window.js";

var resumes

document.addEventListener('DOMContentLoaded', function () {
    getVacancies()
    getProfessions()
    getMyResumes()
})

async function getMyResumes() {
    const userType = getCookie('user_type')
    if (!userType || userType === 'employer') {
        return
    }
    const getMyResumes = await makeRequest({
        method: 'GET',
        url: '/api/resumes/me/'
    })
    resumes = getMyResumes.resumes
}

async function getProfessions() {
    const getResponse = await makeRequest({
        method: 'GET',
        url: '/api/professions'
    })
    const form = document.getElementById('jobForm');
    const jobInput = document.getElementById('job-search');
    const jobsDropdown = document.getElementById('jobsDropdown');

    // Имитация списка IT профессий с сервера в виде объектов
    const availableJobs = getResponse.professions


    // const availableJobs = noSortAvailableJobs.sort((a, b) => a.name.localeCompare(b.name));

    // Function to filter and show matching jobs
    const filterJobs = (searchText) => {
        jobsDropdown.innerHTML = '';
        if (!searchText) {
            jobsDropdown.style.display = 'none';
            return;
        }

        const matchingJobs = availableJobs.filter(job =>
            job.title.toLowerCase().startsWith(searchText.toLowerCase())
        );

        if (matchingJobs.length === 0) {
            jobsDropdown.style.display = 'none';
            return;
        }

        matchingJobs.forEach(job => {
            const option = document.createElement('div');
            option.className = 'job-option';
            option.textContent = job.title;
            option.addEventListener('click', () => {
                jobInput.value = job.title; // Вставка выбранной профессии в input
                jobsDropdown.style.display = 'none';
            });
            jobsDropdown.appendChild(option);
        });

        jobsDropdown.style.display = 'block';
    };

    // Event listener for input changes
    jobInput.addEventListener('input', (e) => {
        filterJobs(e.target.value);
    });

    // Hide dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!jobInput.contains(e.target) && !jobsDropdown.contains(e.target)) {
            jobsDropdown.style.display = 'none';
        }
    });
}


async function getVacancies() {
    const currentUrl = window.location.href;
    const url = new URL(currentUrl);
    const {page} = getUrlParams()

    const profession = url.searchParams.get("profession");
    const city = url.searchParams.get("city")
    const min_salary = url.searchParams.get("min_salary")


    const searchParams = new URLSearchParams();
    searchParams.append('page', page);
    if (profession) {
        searchParams.append('profession', profession);
        document.getElementById('job-search').value = profession
    }
    if (city) {
        searchParams.append('city', city);
        document.getElementById('city').value = city

    }
    if (min_salary) {
        searchParams.append('min_salary', min_salary);
        document.getElementById('salary').value = min_salary
    }


    const loadingIndicator = showLoadingIndicator();
    const getResponse = await makeRequest({
        method: 'GET',
        url: `/api/vacancy/?${searchParams.toString()}`
    })
    console.log(getResponse)
    if (getResponse.vacancies.length === 0) {
        const container = document.getElementById('vacancies-container');
        container.innerHTML = '';
        const countVacancyElement = document.createElement('h2');
        const secondMessage = document.createElement('h3')
        if (profession) {
            countVacancyElement.textContent = `По запросу "${profession}" ничего не найдено`
        } else {
            countVacancyElement.textContent = `По вашему запросу ничего не найдено`
        }
        secondMessage.textContent = ('Попробуйте другие варианты поискового запроса или уберите фильтры')
        container.appendChild(countVacancyElement);
        container.appendChild(secondMessage)
        hideLoadingIndicator(loadingIndicator)
        return
    }
    renderVacancies(getResponse.vacancies, getResponse.can_update, profession, getResponse.count)
    const totalPages = Math.ceil(getResponse.count / 10) // Предполагаем, что на странице 10 вакансий
    createPagination(page, totalPages)
    hideLoadingIndicator(loadingIndicator)
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function renderVacancies(vacancies, can_update, name_vacancy, count_vacancy) {
    const container = document.getElementById('vacancies-container');
    container.innerHTML = '';
    container.style.width = '450px'

    const countVacancyElement = document.createElement('h2');

    if (name_vacancy) {
        countVacancyElement.textContent = `${count_vacancy} вакансий "${name_vacancy}"`
        container.appendChild(countVacancyElement);
    } else {
        countVacancyElement.textContent = ` Найдено ${count_vacancy} вакансий`
        container.appendChild(countVacancyElement);
    }

    vacancies.forEach(vacancy => {
        const vacancyElement = document.createElement('div');
        vacancyElement.classList.add('vacancy');
        vacancyElement.style.width = '150%'

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

        const linkCompany = document.createElement('a')
        linkCompany.innerHTML = vacancy.company.name
        linkCompany.href = apiUrl + `/companies/${vacancy.company.id}`
        linkCompany.style.color = '#666'
        linkCompany.addEventListener('mouseover', function () {
            linkCompany.style.color = 'deepskyblue'; // Цвет текста ссылки при наведении
        });
        linkCompany.addEventListener('mouseout', function () {
            linkCompany.style.color = '#666'; // Цвет текста ссылки при наведении
        });

        const statsLabel = document.createElement('p');
        statsLabel.textContent = 'Статистика:'
        const stastElement = document.createElement('div');
        stastElement.classList.add('stats');
        stastElement.textContent = `0 откликов`

        vacancyElement.appendChild(titleElement);
        vacancyElement.appendChild(updatedAtElement);
        vacancyElement.appendChild(statsLabel);
        vacancyElement.appendChild(stastElement);
        vacancyElement.appendChild(salaryElement);
        vacancyElement.appendChild(cityElement);
        linkElement.appendChild(vacancyElement);

        const userType = getCookie('user_type')

        if (userType === 'worker' || !userType) {
            const feedBack = document.createElement('button');
            feedBack.classList.add('red_button');
            feedBack.style.width = '30%';
            feedBack.textContent = "Откликнуться";

            // Здесь вы должны передать массив резюме для открытия модального окна
            feedBack.onclick = function () {
                event.preventDefault(); // Остановить переход по ссылке
                if (!userType) {
                    window.location.href = apiUrl + '/login';
                    return
                }
                createModal('Выберите резюме для отклика', resumes, vacancy.id);
            };
            vacancyElement.appendChild(feedBack);
        }
        container.appendChild(linkElement);
    });
}

function createPagination(currentPage, totalPages) {
    const paginationElement = document.getElementById("pagination")
    paginationElement.innerHTML = ""

    const maxVisiblePages = 5
    let startPage = Math.max(currentPage - Math.floor(maxVisiblePages / 2), 1)
    const endPage = Math.min(startPage + maxVisiblePages - 1, totalPages)

    if (endPage - startPage + 1 < maxVisiblePages) {
        startPage = Math.max(endPage - maxVisiblePages + 1, 1)
    }

    // Кнопка "Предыдущая"
    const prevButton = document.createElement("button")
    prevButton.textContent = "«"
    prevButton.disabled = currentPage === 1
    prevButton.addEventListener("click", () => changePage(currentPage - 1))
    paginationElement.appendChild(prevButton)

    // Номера страниц
    for (let i = startPage; i <= endPage; i++) {
        const pageLink = document.createElement("button")
        pageLink.href = "#"
        pageLink.textContent = i
        if (i === currentPage) {
            pageLink.classList.add("active")
        }
        pageLink.addEventListener("click", (e) => {
            e.preventDefault()
            changePage(i)
        })
        paginationElement.appendChild(pageLink)
    }

    // Кнопка "Следующая"
    const nextButton = document.createElement("button")
    nextButton.textContent = "»"
    nextButton.disabled = currentPage === totalPages
    nextButton.addEventListener("click", () => changePage(currentPage + 1))
    paginationElement.appendChild(nextButton)

    // Информация о страницах
    const pageInfo = document.createElement("span")
    pageInfo.className = "pagination-info"
    pageInfo.textContent = `${currentPage} из ${totalPages}`
    paginationElement.appendChild(pageInfo)
}

// Функция для изменения страницы
function changePage(newPage) {
    updateUrlParams({page: newPage})
    getVacancies()
    scrollToTop()
}

function getUrlParams() {
    const params = new URLSearchParams(window.location.search);
    return {
        page: parseInt(params.get('page')) || 0
    };
}

// Функция для обновления URL с новыми параметрами
function updateUrlParams(params) {
    const url = new URL(window.location);
    Object.keys(params).forEach(key => {
        url.searchParams.set(key, params[key]);
    });
    window.history.pushState({}, '', url);
}

// Функция для прокрутки страницы вверх
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}


async function searchVacancy() {

    const profession = document.getElementById('job-search').value;
    const city = document.getElementById('city').value
    const min_salary = document.getElementById('salary').value

    const searchParams = new URLSearchParams();
    searchParams.append('page', 1);
    if (profession) {
        searchParams.append('profession', profession);
    }
    if (city) {
        searchParams.append('city', city);
    }
    if (min_salary) {
        searchParams.append('min_salary', min_salary);
    }
    const searchUrl = apiUrl + `/vacancies/?${searchParams.toString()}`;

    window.location.href = searchUrl;
}

async function moveResumes() {
    const searchParams = new URLSearchParams();
    searchParams.append('page', 1);

    const searchUrl = apiUrl + `/resumes/?${searchParams.toString()}`;

    window.location.href = searchUrl;
}

window.moveResumes = moveResumes
window.searchVacancy = searchVacancy