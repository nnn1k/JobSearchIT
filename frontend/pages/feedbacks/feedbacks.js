import {hideLoadingIndicator, showLoadingIndicator} from '/frontend/js/functions_for_loading.js'
import {apiUrl, makeRequest} from '/frontend/js/utils.js';
import {formatDateTime} from "/frontend/js/timefunc.js";
import {showNotification} from "/frontend/js/showNotification.js";

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
        renderFeedbacksForWorker(getResponse.all, 'all_form')
        renderFeedbacksForWorker(getResponse.waiting, 'unread_form')
        renderFeedbacksForWorker(getResponse.accepted, 'invites_form')
        renderFeedbacksForWorker(getResponse.rejected, 'discard_form')
    }
    if (userType === 'employer') {
        renderFeedbacksForEmployer(getResponse.all, 'all_form')
        renderFeedbacksForEmployer(getResponse.waiting, 'unread_form')
        renderFeedbacksForEmployer(getResponse.accepted, 'invites_form')
        renderFeedbacksForEmployer(getResponse.rejected, 'discard_form')
    }
    hideLoadingIndicator(loadingIndicator)
}

function renderFeedbacksForWorker(allFeedbacks, nameForm) {
    const all_feedbacks = document.getElementById(nameForm)
    all_feedbacks.innerHTML = '';
    if (allFeedbacks.length === 0) {
        const countFeedbacks = document.createElement('h2');
        countFeedbacks.textContent = `Тут пока пусто :(`
        all_feedbacks.appendChild(countFeedbacks);
    }

    allFeedbacks.forEach(feedback => {
        const card = document.createElement('div');
        card.className = 'feedback-card';

        // Create card header
        const cardHeader = document.createElement('div');
        cardHeader.className = 'card-header';

        // Create title section
        const titleSection = document.createElement('div');
        titleSection.className = 'title-section';

        // Create title
        const titleElement = document.createElement('h2');
        titleElement.textContent = feedback.vacancy.profession.title;

        // Create subtitle
        const subtitleElement = document.createElement('h3');
        subtitleElement.textContent = feedback.vacancy.company.name;

        // Add title and subtitle to title section
        titleSection.appendChild(titleElement);
        titleSection.appendChild(subtitleElement);

        let statusElement

        if (feedback.is_worker_accepted && feedback.is_employer_accepted) {
            statusElement = document.createElement('a');
            statusElement.className = 'chat-link';
            statusElement.href = '#';
            statusElement.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="chat-icon">
              <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
            </svg>
            Перейти в чат
          `;
            statusElement.href = apiUrl + `/chats/?chatId=${feedback.chat.id}`
        } else if (feedback.is_employer_accepted === false) {
            statusElement = document.createElement('div');
            statusElement.className = 'status-badge status-rejected';
            statusElement.textContent = 'Отказ';
        } else {
            statusElement = document.createElement('div');
            statusElement.className = 'status-badge status-pending';
            statusElement.textContent = 'На рассмотрении';
        }


        // Add title section and status element to header
        cardHeader.appendChild(titleSection);
        cardHeader.appendChild(statusElement);

        // Create card content
        const cardContent = document.createElement('div');
        cardContent.className = 'card-content_2';

        // Create date element
        const dateElement = document.createElement('h4');
        dateElement.className = 'date';
        dateElement.textContent = formatDateTime(feedback.created_at);

        // Add date to card content
        cardContent.appendChild(dateElement);

        // Create delete button
        const deleteButton = document.createElement('button');
        deleteButton.className = 'delete-button';


        // Add trash icon and text to button
        deleteButton.innerHTML = `
    <svg class="delete-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
    </svg>
    Удалить
  `;

        deleteButton.addEventListener('click', function () {
            showNotification('Отклик удален')
            console.log(`Отклик ${feedback.id} удален`);
            const loadingIndicator = showLoadingIndicator();
            makeRequest({
                method: 'DELETE',
                url: `/api/responses/${feedback.id}`
            })
                .then(response => {
                    if (response) {
                        all_feedbacks.removeChild(card);
                        location.reload(true);
                    } else {
                        console.error('Ошибка при удалении отклика');
                    }
                })
                .catch(error => {
                    hideLoadingIndicator(loadingIndicator);
                    console.error('Ошибка:', error);
                });
        })

        // Assemble the card
        card.appendChild(cardHeader);
        card.appendChild(cardContent);
        card.appendChild(deleteButton);

        all_feedbacks.appendChild(card)
    })
}

function renderFeedbacksForEmployer(allFeedbacks, nameForm) {
    const all_feedbacks = document.getElementById(nameForm)
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

        const candidatePosition = document.createElement('a');
        candidatePosition.className = 'candidate-position';
        candidatePosition.textContent = feedback.resume.profession.title;
        candidatePosition.href = apiUrl + `/resumes/${feedback.resume.id}`
        candidatePosition.style.color = 'gray'
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

        if (feedback.is_worker_accepted && feedback.is_employer_accepted) {
            const linkForChat = document.createElement('a')
            linkForChat.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="chat-icon">
              <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
            </svg>
            Перейти в чат
          `;
            linkForChat.href = apiUrl + `/chats/?chatId=${feedback.chat.id}`
            linkForChat.style.marginLeft = '85%'
            linkForChat.className = 'chat-link'
            cardContent.appendChild(jobTitleHeader);
            cardContent.appendChild(candidateBlock);
            cardContent.appendChild(linkForChat)
            card.appendChild(cardContent);
            all_feedbacks.appendChild(card);
            return
        }

        if (feedback.is_employer_accepted === false) {
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
        rejectButton.innerHTML = `Отклонить`;
        rejectButton.style.width = '20%'

        // Кнопка "Одобрить"
        const approveButton = document.createElement('button');
        approveButton.className = 'red_button';
        approveButton.innerHTML = `Одобрить`;
        approveButton.style.width = '20%'

        // Добавляем кнопки в контейнер
        actionButtons.appendChild(rejectButton);
        actionButtons.appendChild(approveButton);

        // Собираем всю карточку
        cardContent.appendChild(jobTitleHeader);
        cardContent.appendChild(candidateBlock);
        cardContent.appendChild(actionButtons);
        card.appendChild(cardContent);


        rejectButton.addEventListener('click', function () {
            const loadingIndicator = showLoadingIndicator();
            showNotification('Отклик отклонен')
            makeRequest({
                method: 'POST',
                url: `/api/responses/${feedback.id}/reject`
            })
                .then(response => {
                    hideLoadingIndicator(loadingIndicator);
                    if (response) {
                        location.reload(true);
                    } else {
                        console.error('Ошибка');
                    }
                })
                .catch(error => {
                    hideLoadingIndicator(loadingIndicator);
                    console.error('Ошибка:', error);
                });
        });

        approveButton.addEventListener('click', function () {
            const loadingIndicator = showLoadingIndicator();
            showNotification('Отклик одобрен')
            makeRequest({
                method: 'POST',
                url: `/api/responses/${feedback.id}/accept`
            })
                .then(response => {
                    hideLoadingIndicator(loadingIndicator);
                    if (response) {
                        location.reload(true);
                    } else {
                        console.error('Ошибка');
                    }
                })
                .catch(error => {
                    hideLoadingIndicator(loadingIndicator);
                    console.error('Ошибка:', error);
                });
        });


        all_feedbacks.appendChild(card);
    });
}


window.showForm = showForm