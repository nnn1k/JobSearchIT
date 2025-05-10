import {apiUrl, makeRequest} from "/frontend/js/utils.js";
import {print_salary} from "/frontend/js/print_salary.js";
import {formatDateTime} from "/frontend/js/timefunc.js";
import {hideLoadingIndicator, showLoadingIndicator} from '/frontend/js/functions_for_loading.js'
import {createModal} from "/frontend/js/modal_window.js";


let reviews
let resumes

function calculateAverageRating() {
    if (reviews === 0) {
        return;
    }
    const sum = reviews.reduce((total, review) => total + review.score, 0);
    return (sum / reviews.length).toFixed(1);
}

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
        url: '/api/resumes/me/'
    })
    resumes = getMyResumes.resumes
}

async function getReviews() {
    const company_id = location.pathname.split('/')[2]
    const getResponse = await makeRequest({
        method: 'GET',
        url: `/api/companies/${company_id}/reviews`
    })
    reviews = getResponse.reviews
    console.log(reviews)
    updateRatingDisplay()

}

document.addEventListener('DOMContentLoaded', function () {
    getMyResumes()
    get_company()
    getReviews()
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
        width: 700,
        height: 600,
        fontsize: 50,
        whiteSpace: "pre-wrap"
    });
    hideLoadingIndicator(loadingIndicator);
    tinymce.get('company_description_update').setContent(getResponse.company.description)
    document.getElementById('company_description_update').value = getResponse.company.description;
    console.log(getResponse.company.vacancies)
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

    if (vacancies.length === 0) {
        const countVacancies = document.createElement('h2');
        countVacancies.textContent = `У компании пока нет вакансий :(`
        container.appendChild(countVacancies);
        return
    }

    vacancies.forEach(vacancy => {
        const vacancyElement = document.createElement('div');
        vacancyElement.classList.add('vacancy');

        const linkElement = document.createElement('a');
        linkElement.href = `/vacancies/${vacancy.id}`;
        linkElement.style.color = '#555'

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

        vacancyElement.appendChild(titleElement);
        vacancyElement.appendChild(updatedAtElement);
        vacancyElement.appendChild(statsLabel);
        vacancyElement.appendChild(stastElement);
        vacancyElement.appendChild(salaryElement);
        vacancyElement.appendChild(cityElement);


        const userType = getCookie('user_type')

        if (userType === 'worker' || !userType) {
            const feedbackButton = document.createElement('button');
            feedbackButton.classList.add('red_button');
            feedbackButton.style.width = '30%';
            feedbackButton.textContent = "Откликнуться";
            feedbackButton.onclick = function () {
                event.preventDefault(); // Остановить переход по ссылке
                if (!userType) {
                    window.location.href = apiUrl + '/login';
                    return
                }
                createModal('Выберите резюме для отклика', resumes, vacancy.id);
            };
            vacancyElement.appendChild(feedbackButton);
            linkElement.appendChild(vacancyElement);
            container.appendChild(linkElement);
            return;
        }

        if (can_update) {
            const editButton = document.createElement('button');
            editButton.classList.add('red_button');
            editButton.style.width = '30%';
            editButton.textContent = "Редактировать";
            editButton.onclick = () => {
                window.location.href = `/vacancies/${vacancy.id}/edit`;
            };
            vacancyElement.appendChild(editButton);
            linkElement.appendChild(vacancyElement);
            container.appendChild(linkElement);
            return;
        }
        linkElement.appendChild(vacancyElement)
        container.appendChild(linkElement);
    });
}

// Данные отзывов (в реальном проекте это будет храниться на сервере)


// Параметры пагинации
const reviewsPerPage = 5;
let currentPage = 1;

// DOM элементы
const ratingValueElement = document.getElementById('rating-value');
const starsElement = document.getElementById('stars');
const reviewsCountElement = document.getElementById('reviews-count');
const reviewsModal = document.getElementById('reviews-modal');
const closeModalButton = document.getElementById('close-modal');
const reviewsList = document.getElementById('reviews-list');
const noReviewsMessage = document.getElementById('no-reviews');
const newReviewForm = document.getElementById('new-review-form');
const paginationContainer = document.getElementById('pagination-container');

// Функция для расчета среднего рейтинга


// Функция для отображения звезд на основе рейтинга
function displayStars(rating) {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating - fullStars >= 0.5;

    let starsHTML = '';

    // Полные звезды
    for (let i = 0; i < fullStars; i++) {
        starsHTML += '<span style="color: var(--red);">★</span>';
    }

    // Половина звезды
    if (hasHalfStar) {
        starsHTML += '<span style="color: var(--red);">★</span>';
        fullStars++;
    }

    // Пустые звезды
    for (let i = fullStars + (hasHalfStar ? 0 : 0); i < 5; i++) {
        starsHTML += '<span style="color: #ddd;">★</span>';
    }

    return starsHTML;
}

// Функция для обновления отображения рейтинга
function updateRatingDisplay() {
    const averageRating = calculateAverageRating();
    console.log(averageRating)
    ratingValueElement.textContent = averageRating;
    starsElement.innerHTML = displayStars(averageRating);

    const reviewsText = reviews.length === 1 ? 'отзыв' :
        (reviews.length >= 2 && reviews.length <= 4) ? 'отзыва' : 'отзывов';
    reviewsCountElement.textContent = `${reviews.length} ${reviewsText}`;
}

// Функция для создания элементов пагинации
function createPagination() {
    const totalPages = Math.ceil(reviews.length / reviewsPerPage);

    if (totalPages <= 1) {
        paginationContainer.innerHTML = '';
        return;
    }

    let paginationHTML = '';

    // Кнопка "Предыдущая"
    paginationHTML += `
                <button class="pagination-button" id="prev-page" ${currentPage === 1 ? 'disabled' : ''}>
                    &laquo;
                </button>
            `;

    // Номера страниц
    for (let i = 1; i <= totalPages; i++) {
        paginationHTML += `
                    <button class="pagination-button ${currentPage === i ? 'active' : ''}" data-page="${i}">
                        ${i}
                    </button>
                `;
    }

    // Кнопка "Следующая"
    paginationHTML += `
                <button class="pagination-button" id="next-page" ${currentPage === totalPages ? 'disabled' : ''}>
                    &raquo;
                </button>
            `;

    paginationContainer.innerHTML = paginationHTML;

    // Добавление обработчиков событий для кнопок пагинации
    document.querySelectorAll('.pagination-button[data-page]').forEach(button => {
        button.addEventListener('click', function () {
            currentPage = parseInt(this.getAttribute('data-page'));
            displayReviews();
        });
    });

    // Обработчик для кнопки "Предыдущая"
    const prevButton = document.getElementById('prev-page');
    if (prevButton) {
        prevButton.addEventListener('click', function () {
            if (currentPage > 1) {
                currentPage--;
                displayReviews();
            }
        });
    }

    // Обработчик для кнопки "Следующая"
    const nextButton = document.getElementById('next-page');
    if (nextButton) {
        nextButton.addEventListener('click', function () {
            if (currentPage < totalPages) {
                currentPage++;
                displayReviews();
            }
        });
    }
}

// Функция для отображения списка отзывов с учетом пагинации
function displayReviews() {
    if (reviews.length === 0) {
        noReviewsMessage.style.display = 'block';
        reviewsList.innerHTML = '';
        paginationContainer.innerHTML = '';
        return;
    }

    noReviewsMessage.style.display = 'none';

    // Сортировка отзывов по дате (новые сверху)
    const sortedReviews = [...reviews].sort((a, b) => b.date - a.date);

    // Получение отзывов для текущей страницы
    const startIndex = (currentPage - 1) * reviewsPerPage;
    const endIndex = startIndex + reviewsPerPage;
    const currentPageReviews = sortedReviews.slice(startIndex, endIndex);

    let reviewsHTML = '';
    console.log(currentPageReviews)
    currentPageReviews.forEach(review => {
        const date = new Date(review.date);
        const formattedDate = `${date.getDate().toString().padStart(2, '0')}.${(date.getMonth() + 1).toString().padStart(2, '0')}.${date.getFullYear()}`;
        console.log(review)
        reviewsHTML += `
                    <div class="review-item">
                        <div class="review-header">
                            <span class="review-author">${review.worker.name} ${review.worker.surname}</span>
                            <span class="review-rating">${'★'.repeat(review.score)}</span>
                        </div>
                        <div class="review-text">${review.message}</div>
                        <div class="review-date" style="font-size: 12px; color: #777; margin-top: 10px;">${formatDateTime(review.created_at)}</div>
                    </div>
                `;
    });

    reviewsList.innerHTML = reviewsHTML;

    createPagination();
}

// Обработчик события для открытия модального окна
reviewsCountElement.addEventListener('click', function () {
    reviewsModal.style.display = 'block';
    currentPage = 1; // Сбрасываем на первую страницу при открытии
    displayReviews();
    document.body.style.overflow = 'hidden'; // Предотвращает прокрутку страницы
});

// Обработчик события для закрытия модального окна
closeModalButton.addEventListener('click', function () {
    reviewsModal.style.display = 'none';
    document.body.style.overflow = ''; // Восстанавливает прокрутку страницы
});

// Закрытие модального окна при клике вне его содержимого
window.addEventListener('click', function (event) {
    if (event.target === reviewsModal) {
        reviewsModal.style.display = 'none';
        document.body.style.overflow = '';
    }
});

// Обработчик отправки формы нового отзыва
newReviewForm.addEventListener('submit', function (event) {
    event.preventDefault();

    const ratingInput = document.querySelector('input[name="rating"]:checked');
    console.log(ratingInput.value)
    const message = document.getElementById('review-text').value;

    if (!ratingInput) {
        alert('Пожалуйста, выберите оценку');
        return;
    }

    const score = parseInt(ratingInput.value);
    const company_id = location.pathname.split('/')[2]

    const loadingIndicator = showLoadingIndicator();
    const postResponse = makeRequest({
        method: 'POST',
        url: `/api/companies/${company_id}/reviews`,
        data: {
            score,
            message
        }
    })
    hideLoadingIndicator(loadingIndicator)

    updateRatingDisplay();
    currentPage = 1;
    displayReviews();
    newReviewForm.reset();

});


window.update_company = update_company
window.showForm = showForm