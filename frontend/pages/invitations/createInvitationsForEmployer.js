import {formatDateTime} from "/frontend/js/timefunc.js";
import {showNotification} from "../../js/showNotification.js";
import {hideLoadingIndicator, showLoadingIndicator} from "../../js/functions_for_loading.js";
import {apiUrl, makeRequest} from "../../js/utils.js";

export function createInviteForEmployer(invite) {
    // Create the main card element
    const card = document.createElement('div');
    card.className = 'card';

    // Create card header
    const cardHeader = document.createElement('div');
    cardHeader.className = 'card-header';

    // Create card title section
    const cardTitle = document.createElement('div');
    cardTitle.className = 'card-title';

    const name = document.createElement('h3');
    name.textContent = invite.resume.worker.name + ' ' + invite.resume.worker.surname;

    const position = document.createElement('p');
    position.textContent = invite.resume.profession.title;

    cardTitle.appendChild(name);
    cardTitle.appendChild(position);

    // Create badge
    if (invite.is_employer_accepted && invite.is_worker_accepted) {
        const linkForChat = document.createElement('a');
        linkForChat.className = 'chat-link';
        linkForChat.href = '#';
        linkForChat.innerHTML = `
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="chat-icon">
            <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
          </svg>
          Перейти в чат
        `;
        linkForChat.href = apiUrl + `/chats/?chatId=${invite.chat.id}`
        cardHeader.appendChild(cardTitle);
        cardHeader.appendChild(linkForChat);
    }
    if (invite.is_worker_accepted === false) {
        const badge = document.createElement('div');
        badge.className = `badge badge-declined`;
        badge.textContent = 'Отклонено';
        cardHeader.appendChild(cardTitle);
        cardHeader.appendChild(badge);
    }
    if (invite.is_worker_accepted === null){
        const badge = document.createElement('div');
        badge.className = `badge badge-pending`;
        badge.textContent = 'На рассмотрении';
        cardHeader.appendChild(cardTitle);
        cardHeader.appendChild(badge);
    }


    // Create card content
    const cardContent = document.createElement('div');
    cardContent.className = 'card-content';

    // Create first info row - job invitation
    const jobInfo = document.createElement('div');
    jobInfo.className = 'card-info';

    const userIcon = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    userIcon.setAttribute('class', 'icon');
    userIcon.setAttribute('viewBox', '0 0 24 24');

    const userPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    userPath.setAttribute('d', 'M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2M12 11a4 4 0 100-8 4 4 0 000 8z');
    userPath.setAttribute('stroke', 'currentColor');
    userPath.setAttribute('stroke-width', '2');
    userPath.setAttribute('stroke-linecap', 'round');
    userPath.setAttribute('stroke-linejoin', 'round');
    userPath.setAttribute('fill', 'none');

    userIcon.appendChild(userPath);

    const jobText = document.createElement('span');
    jobText.innerHTML = `Приглашен на вакансию: <strong>${invite.vacancy.profession.title}</strong>`;

    jobInfo.appendChild(userIcon);
    jobInfo.appendChild(jobText);

    // Create second info row - date
    const dateInfo = document.createElement('div');
    dateInfo.className = 'card-info';

    const calendarIcon = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    calendarIcon.setAttribute('class', 'icon');
    calendarIcon.setAttribute('viewBox', '0 0 24 24');

    const calendarPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    calendarPath.setAttribute('d', 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z');
    calendarPath.setAttribute('stroke', 'currentColor');
    calendarPath.setAttribute('stroke-width', '2');
    calendarPath.setAttribute('stroke-linecap', 'round');
    calendarPath.setAttribute('stroke-linejoin', 'round');
    calendarPath.setAttribute('fill', 'none');

    calendarIcon.appendChild(calendarPath);

    const dateText = document.createElement('span');
    dateText.textContent = `Приглашение отправлено: ${formatDateTime(invite.created_at)}`;

    dateInfo.appendChild(calendarIcon);
    dateInfo.appendChild(dateText);

    // Create actions section
    const actions = document.createElement('div');
    actions.className = 'employer-actions';

    const spacer = document.createElement('div');

    const deleteButton = document.createElement('button');
    deleteButton.className = 'red_button';
    deleteButton.textContent = 'Удалить';
    deleteButton.style.width = '20%'

    deleteButton.addEventListener('click', function () {
            showNotification('Приглашения удалено')
            console.log(`Отклик ${invite.id} удален`);
            const loadingIndicator = showLoadingIndicator();
            makeRequest({
                method: 'DELETE',
                url: `/api/responses/${invite.id}`
            })
                .then(response => {
                    if (response) {
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

    actions.appendChild(spacer);
    actions.appendChild(deleteButton);

    // Assemble the card
    cardContent.appendChild(jobInfo);
    cardContent.appendChild(dateInfo);
    cardContent.appendChild(actions);

    card.appendChild(cardHeader);
    card.appendChild(cardContent);

    return card;
}

window.createInviteForEmployer = createInviteForEmployer