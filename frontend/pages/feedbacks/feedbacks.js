import {hideLoadingIndicator, showLoadingIndicator} from '/frontend/js/functions_for_loading.js'
import {apiUrl, makeRequest} from '/frontend/js/utils.js';
import {formatDateTime} from "/frontend/js/timefunc.js";

document.addEventListener('DOMContentLoaded', function () {
    const first_button = document.getElementById('switch_all')
    showForm('all_form', first_button)
    getFeedbacks()
})

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
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

async function getFeedbacks() {
    const loadingIndicator = showLoadingIndicator();
    const getResponse = await makeRequest({
        method: 'GET',
        url: `/api/responses/response`
    })
    console.log(getResponse)

    const userType = getCookie('user_type')
    if (userType === 'worker') {
        renderFeedbacksForWorker(getResponse.all, getResponse.accepted, getResponse.rejected, getResponse.waiting)
    }
    if (userType === 'employer') {
        renderFeedbacksForEmployer(getResponse.all)
    }
    hideLoadingIndicator(loadingIndicator)
}

function renderFeedbacksForWorker(allFeedbacks, acceptedFeedback, rejectedFeedback, waitingFeedback) {
    const all_feedbacks = document.getElementById('all_form')
    all_feedbacks.innerHTML = '';
    if (allFeedbacks.length === 0) {
        const countFeedbacks = document.createElement('h2');
        countFeedbacks.textContent = `Тут пока пусто :(`
        all_feedbacks.appendChild(countFeedbacks);
    }
    allFeedbacks.forEach(feedback => {
        const feedbackElement = document.createElement('div');
        feedbackElement.classList = 'feedback'

        const titleVacancy = document.createElement('h2');
        titleVacancy.textContent = feedback.vacancy.profession.title
        const nameCompany = document.createElement('h3');
        nameCompany.textContent = feedback.vacancy.company.name
        const createAt = document.createElement('p')
        createAt.textContent = formatDateTime(feedback.created_at)
        const deleteBtn = document.createElement('button')
        deleteBtn.textContent = 'Удалить'
        deleteBtn.classList = 'red_button'
        deleteBtn.style.marginLeft = '70%'
        deleteBtn.style.width = '25%'
        feedbackElement.appendChild(titleVacancy)
        feedbackElement.appendChild(nameCompany)
        feedbackElement.appendChild(createAt)
        if (feedback.is_worker_accepted && feedback.is_employer_accepted) {
            const linkForChat = document.createElement('a')
            linkForChat.textContent = 'Перейти в чат'
            linkForChat.href = '#'
            feedbackElement.appendChild(linkForChat)
        }
        feedbackElement.appendChild(deleteBtn)
        all_feedbacks.appendChild(feedbackElement)
    });

    const accepted_feedbacks = document.getElementById('invites_form')
    accepted_feedbacks.innerHTML = ''
    if (acceptedFeedback.length === 0) {
        const countFeedbacks = document.createElement('h2');
        countFeedbacks.textContent = `Тут пока пусто :(`
        accepted_feedbacks.appendChild(countFeedbacks);
    }
    acceptedFeedback.forEach(feedback => {
        const feedbackElement = document.createElement('div');
        feedbackElement.classList = 'feedback'

        const titleVacancy = document.createElement('h2');
        titleVacancy.textContent = feedback.vacancy.profession.title
        const nameCompany = document.createElement('h3');
        nameCompany.textContent = feedback.vacancy.company.name
        const createAt = document.createElement('p')
        createAt.textContent = formatDateTime(feedback.created_at)
        const linkForChat = document.createElement('a')
        linkForChat.textContent = 'Перейти в чат'
        linkForChat.href = '#'
        const deleteBtn = document.createElement('button')
        deleteBtn.textContent = 'Удалить'
        deleteBtn.classList = 'red_button'
        deleteBtn.style.marginLeft = '70%'
        deleteBtn.style.width = '25%'
        feedbackElement.appendChild(titleVacancy)
        feedbackElement.appendChild(nameCompany)
        feedbackElement.appendChild(createAt)
        feedbackElement.appendChild(linkForChat)
        feedbackElement.appendChild(deleteBtn)
        accepted_feedbacks.appendChild(feedbackElement)
    });

    const rejected_feedbacks = document.getElementById('discard_form')
    rejected_feedbacks.innerHTML = ''
    if (rejectedFeedback.length === 0) {
        const countFeedbacks = document.createElement('h2');
        countFeedbacks.textContent = `Тут пока пусто :(`
        rejected_feedbacks.appendChild(countFeedbacks);
    }
    rejectedFeedback.forEach(feedback => {
        const feedbackElement = document.createElement('div');
        feedbackElement.classList = 'feedback'

        const titleVacancy = document.createElement('h2');
        titleVacancy.textContent = feedback.vacancy.profession.title
        const nameCompany = document.createElement('h3');
        nameCompany.textContent = feedback.vacancy.company.name
        const createAt = document.createElement('p')
        createAt.textContent = formatDateTime(feedback.created_at)
        const deleteBtn = document.createElement('button')
        deleteBtn.textContent = 'Удалить'
        deleteBtn.classList = 'red_button'
        deleteBtn.style.marginLeft = '70%'
        deleteBtn.style.width = '25%'
        feedbackElement.appendChild(titleVacancy)
        feedbackElement.appendChild(nameCompany)
        feedbackElement.appendChild(createAt)
        feedbackElement.appendChild(deleteBtn)
        rejected_feedbacks.appendChild(feedbackElement)
    });

    const waiting_feedbacks = document.getElementById('unread_form')
    waiting_feedbacks.innerHTML = ''
    if (waitingFeedback.length === 0) {
        const countFeedbacks = document.createElement('h2');
        countFeedbacks.textContent = `Тут пока пусто :(`
        waiting_feedbacks.appendChild(countFeedbacks);
    }
    waitingFeedback.forEach(feedback => {
        const feedbackElement = document.createElement('div');
        feedbackElement.classList = 'feedback'

        const titleVacancy = document.createElement('h2');
        titleVacancy.textContent = feedback.vacancy.profession.title
        const nameCompany = document.createElement('h3');
        nameCompany.textContent = feedback.vacancy.company.name
        const createAt = document.createElement('p')
        createAt.textContent = formatDateTime(feedback.created_at)
        const deleteBtn = document.createElement('button')
        deleteBtn.textContent = 'Удалить'
        deleteBtn.classList = 'red_button'
        deleteBtn.style.marginLeft = '70%'
        deleteBtn.style.width = '25%'
        feedbackElement.appendChild(titleVacancy)
        feedbackElement.appendChild(nameCompany)
        feedbackElement.appendChild(createAt)
        feedbackElement.appendChild(deleteBtn)
        waiting_feedbacks.appendChild(feedbackElement)
    });
}

function renderFeedbacksForEmployer(allFeedbacks) {
    const all_feedbacks = document.getElementById('all_form')
    if (allFeedbacks.length === 0) {
        const countFeedbacks = document.createElement('h2');
        countFeedbacks.textContent = `Тут пока пусто :(`
        all_feedbacks.appendChild(countFeedbacks);
    }
    allFeedbacks.forEach(feedback => {
        const card = document.createElement('div');
        card.className = 'card';

        const cardContent = document.createElement('div');
        cardContent.className = 'card-content';

        // Создаем заголовок с информацией о вакансии
        const jobTitleHeader = document.createElement('div');
        jobTitleHeader.className = 'job-title-header';

        const jobTitleIcon = document.createElement('div');
        jobTitleIcon.className = 'job-title-icon';
        jobTitleIcon.innerHTML = `
    <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
        <line x1="8" y1="21" x2="16" y2="21"></line>
        <line x1="12" y1="17" x2="12" y2="21"></line>
    </svg>
  `;

        const linkVacancy = document.createElement('a')
        linkVacancy.textContent = `  ${feedback.vacancy.profession.title}`
        linkVacancy.href = apiUrl + `/vacancies/${feedback.vacancy.id}`
        linkVacancy.style.color = 'gray'

        const jobTitle = document.createElement('span');
        jobTitle.className = 'job-title';
        jobTitle.textContent = `Вакансия:`;
        jobTitle.appendChild(linkVacancy)

        // Собираем заголовок
        jobTitleHeader.appendChild(jobTitleIcon);
        jobTitleHeader.appendChild(jobTitle);

        // Создаем блок с информацией о кандидате
        const candidateBlock = document.createElement('div');
        candidateBlock.className = 'candidate';

        // Информация о кандидате
        const candidateInfo = document.createElement('div');
        candidateInfo.className = 'candidate-info';

        const candidateName = document.createElement('h3');
        candidateName.className = 'candidate-name';
        candidateName.textContent = `${feedback.resume.worker.name} ${feedback.resume.worker.surname}`;

        const candidatePosition = document.createElement('p');
        candidatePosition.className = 'candidate-position';
        candidatePosition.textContent = feedback.resume.profession.title;

        const skillsContainer = document.createElement('div');
        skillsContainer.className = 'skills';

        // Добавляем навыки
        feedback.resume.skills.forEach(skill => {
            const skillBadge = document.createElement('span');
            skillBadge.className = 'badge badge-secondary';
            skillBadge.textContent = skill.name;
            skillsContainer.appendChild(skillBadge);
        });

        // Собираем информацию о кандидате
        candidateInfo.appendChild(candidateName);
        candidateInfo.appendChild(candidatePosition);
        candidateInfo.appendChild(skillsContainer);

        // Метаданные кандидата
        const candidateMeta = document.createElement('div');
        candidateMeta.className = 'candidate-meta';

        const metaItem = document.createElement('div');
        metaItem.className = 'meta-item';
        metaItem.innerHTML = `
    <svg class="icon icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <polyline points="12 6 12 12 16 14"></polyline>
    </svg>
    <span>Дата отклика: ${formatDateTime(feedback.created_at)}</span>
  `;

        // Статус кандидата
        const statusBadge = document.createElement('span');
        statusBadge.className = `badge badge-status badge-${feedback.status}`;

        let statusText = 'На рассмотрении';

        if (feedback.is_worker_accepted && feedback.is_employer_accepted) {
            statusText = 'Одобрено'
        }
        if (feedback.is_employer_accepted === false) {
            statusText = 'Отказ'
        }

        statusBadge.textContent = statusText;

        // Собираем метаданные
        candidateMeta.appendChild(metaItem);
        candidateMeta.appendChild(statusBadge);

        // Добавляем информацию и метаданные в блок кандидата
        candidateBlock.appendChild(candidateInfo);
        candidateBlock.appendChild(candidateMeta);

        if (feedback.is_worker_accepted && feedback.is_employer_accepted){
            const linkForChat = document.createElement('a')
            linkForChat.textContent = 'Перейти в чат'
            linkForChat.href = '#'
            linkForChat.style.marginLeft = '85%'
            cardContent.appendChild(jobTitleHeader);
            cardContent.appendChild(candidateBlock);
            cardContent.appendChild(linkForChat)
            card.appendChild(cardContent);
            all_feedbacks.appendChild(card);
            return
        }

        if (feedback.is_employer_accepted === false){
            cardContent.appendChild(jobTitleHeader);
            cardContent.appendChild(candidateBlock);
            card.appendChild(cardContent);
            all_feedbacks.appendChild(card);
            return
        }
        // Создаем кнопки действий
        const actionButtons = document.createElement('div');
        actionButtons.className = 'action-buttons';

        // Кнопка "Отклонить"
        const rejectButton = document.createElement('button');
        rejectButton.className = 'white_button';
        rejectButton.innerHTML = `
    Отклонить
  `;
        rejectButton.style.width = '20%'

        // Кнопка "Одобрить"
        const approveButton = document.createElement('button');
        approveButton.className = 'red_button';
        approveButton.innerHTML = `
    Одобрить
  `;
        approveButton.style.width = '20%'

        // Добавляем кнопки в контейнер
        actionButtons.appendChild(rejectButton);
        actionButtons.appendChild(approveButton);

        // Собираем всю карточку
        cardContent.appendChild(jobTitleHeader);
        cardContent.appendChild(candidateBlock);
        cardContent.appendChild(actionButtons);
        card.appendChild(cardContent);


        // rejectButton.addEventListener('click', function () {
        //     console.log(`Кандидат ${candidate.name} отклонен`);
        //     // Здесь можно добавить логику для отклонения кандидата
        //     statusBadge.className = 'badge badge-status badge-rejected';
        //     statusBadge.textContent = 'Отклонено';
        // });
        //
        // approveButton.addEventListener('click', function () {
        //     console.log(`Кандидат ${candidate.name} одобрен`);
        //     // Здесь можно добавить логику для одобрения кандидата
        //     statusBadge.className = 'badge badge-status badge-approved';
        //     statusBadge.textContent = 'Одобрено';
        // });


        all_feedbacks.appendChild(card);
    });
}


window.showForm = showForm