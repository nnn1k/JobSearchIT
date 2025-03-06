import {apiUrl, makeRequest} from '/frontend/js/utils.js';
import {hideLoadingIndicator, showLoadingIndicator} from '/frontend/js/functions_for_loading.js'
import {print_salary} from "/frontend/js/print_salary.js";
import {formatDateTime} from "/frontend/js/timefunc.js";

document.addEventListener('DOMContentLoaded', function () {
    getResumes()
    getProfessions()
})

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
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

async function getResumes(){
    const currentUrl = window.location.href;
    const url = new URL(currentUrl);
    const { page, size } = getUrlParams()

    const profession = url.searchParams.get("profession");
    const city =  url.searchParams.get("city")
    const max_salary =  url.searchParams.get("max_salary")


    const searchParams = new URLSearchParams();
    searchParams.append('page', page);
    if (profession){
        searchParams.append('profession', profession);
        document.getElementById('job-search').value = profession
    }
    if (city){
        searchParams.append('city', city);
        document.getElementById('city').value = city

    }
    if (max_salary){
        searchParams.append('max_salary', max_salary);
        document.getElementById('salary').value = max_salary
    }



    const loadingIndicator = showLoadingIndicator();
    const getResponse = await makeRequest({
        method: 'GET',
        url: `/api/resumes/?${searchParams.toString()}`
    })
    console.log(getResponse)
    if (getResponse.resumes.length === 0){
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
    renderResumes(getResponse.resumes, profession ,getResponse.count)
    const totalPages = Math.ceil(getResponse.count / 10) // Предполагаем, что на странице 10 вакансий
    createPagination(page, totalPages)
    hideLoadingIndicator(loadingIndicator)
}

function renderResumes(vacancies, name_vacancy, count_vacancy) {
    const container = document.getElementById('vacancies-container');
    container.innerHTML = '';
    container.style.width = '450px'

    const countVacancyElement = document.createElement('h2');

    if (name_vacancy){
        countVacancyElement.textContent = `${count_vacancy} резюме "${name_vacancy}"`
        container.appendChild(countVacancyElement);
    }
    else{
        countVacancyElement.textContent = ` Найдено ${count_vacancy} резюме`
        container.appendChild(countVacancyElement);
    }
    vacancies.forEach(vacancy => {
        const vacancyElement = document.createElement('div');
        vacancyElement.classList.add('vacancy');
        vacancyElement.style.width = '150%'

        const linkElement = document.createElement('a');
        linkElement.href = `/resumes/${vacancy.id}`;
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
        stastElement.textContent = `0 приглашений`

        vacancyElement.appendChild(titleElement);
        vacancyElement.appendChild(updatedAtElement);
        vacancyElement.appendChild(statsLabel);
        vacancyElement.appendChild(stastElement);
        vacancyElement.appendChild(salaryElement);
        vacancyElement.appendChild(cityElement);
        linkElement.appendChild(vacancyElement);

        const userType = getCookie('user_type')

        if (userType === 'employer' || !userType) {
            const feedBack = document.createElement('button');
            feedBack.classList.add('red_button');
            feedBack.style.width = '30%';
            feedBack.textContent = "Пригласить";
            vacancyElement.appendChild(feedBack);
            container.appendChild(linkElement);
            return;
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
  updateUrlParams({ page: newPage })
  getResumes()
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

async function searchResume(){

    const profession = document.getElementById('job-search').value;
    const city = document.getElementById('city').value
    const max_salary = document.getElementById('salary').value

    const searchParams = new URLSearchParams();
    searchParams.append('page', 1);
    if (profession){
        searchParams.append('profession', profession);
    }
    if (city){
        searchParams.append('city', city);
    }
    if (max_salary){
        searchParams.append('max_salary', max_salary);
    }
    const searchUrl = apiUrl + `/resumes/?${searchParams.toString()}`;

    window.location.href = searchUrl;
}

async function moveVacancies() {
    const searchParams = new URLSearchParams();
    searchParams.append('page', 1);

    const searchUrl = apiUrl + `/vacancies/?${searchParams.toString()}`;

    window.location.href = searchUrl;
}

window.searchResume = searchResume
window.moveVacancies = moveVacancies