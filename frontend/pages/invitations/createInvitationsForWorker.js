import {hideLoadingIndicator, showLoadingIndicator} from "../../js/functions_for_loading.js";
import {showNotification} from "../../js/showNotification.js";
import {apiUrl, makeRequest} from "../../js/utils.js";

export function createInvitationCard(company, position, date, resume, is_employer_accepted, is_worker_accepted, id, chatId) {

  // Create main card container
  const card = document.createElement('div');
  card.className = 'card';

  // Create card header
  const cardHeader = document.createElement('div');
  cardHeader.className = 'card-header';

  const cardFooter = document.createElement('div');
  cardFooter.className = 'card-footer';

  // Create card title section
  const cardTitle = document.createElement('div');
  cardTitle.className = 'card-title';

  const companyTitle = document.createElement('h3');
  companyTitle.textContent = company;

  const positionText = document.createElement('p');
  positionText.textContent = position;

  cardTitle.appendChild(companyTitle);
  cardTitle.appendChild(positionText);

  // Create status badge
  const badge = document.createElement('div');
  badge.className = 'badge badge-pending';
  if (!is_worker_accepted){
    badge.textContent = 'На рассмотрении';
    cardHeader.appendChild(cardTitle);
    cardHeader.appendChild(badge);
  }
  if (is_worker_accepted === true && is_employer_accepted === true){
    badge.textContent = 'Принято';
    badge.className = 'badge badge-accepted'
    const linkForChat = document.createElement('a');
    linkForChat.className = 'chat-link';
    linkForChat.href = '#';
    linkForChat.innerHTML = `
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="chat-icon">
            <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
          </svg>
          Перейти в чат
        `;
    linkForChat.href = apiUrl + `/chats/?chatId=${chatId}`
    cardHeader.appendChild(cardTitle);
    cardHeader.appendChild(badge);
    cardFooter.appendChild(linkForChat);
  }
  if (is_worker_accepted === false){
    badge.textContent = 'Отклонено';
    badge.className = 'badge badge-declined'
    cardHeader.appendChild(cardTitle);
    cardHeader.appendChild(badge);
  }


  // Create card content
  const cardContent = document.createElement('div');
  cardContent.className = 'card-content';

  // Create date info
  const dateInfo = document.createElement('div');
  dateInfo.className = 'card-info';

  // Create calendar icon
  const calendarIcon = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  calendarIcon.setAttribute('class', 'icon');
  calendarIcon.setAttribute('viewBox', '0 0 24 24');
  calendarIcon.setAttribute('xmlns', 'http://www.w3.org/2000/svg');

  const iconPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  iconPath.setAttribute('d', 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z');
  iconPath.setAttribute('stroke', 'currentColor');
  iconPath.setAttribute('stroke-width', '2');
  iconPath.setAttribute('stroke-linecap', 'round');
  iconPath.setAttribute('stroke-linejoin', 'round');
  iconPath.setAttribute('fill', 'none');

  calendarIcon.appendChild(iconPath);

  const dateText = document.createElement('span');
  dateText.textContent = `Приглашение отправлено: ${date}`;

  dateInfo.appendChild(calendarIcon);
  dateInfo.appendChild(dateText);

  // Create resume info
  const resumeInfo = document.createElement('div');
  resumeInfo.className = 'card-info';

  const resumeText = document.createElement('span');
  resumeText.textContent = `Резюме: ${resume}`;

  resumeInfo.appendChild(resumeText);

  // Append info sections to content
  cardContent.appendChild(dateInfo);
  cardContent.appendChild(resumeInfo);

  if ((is_worker_accepted === true && is_employer_accepted === true) || is_worker_accepted === false){
    card.appendChild(cardHeader);
    card.appendChild(cardContent);
    card.appendChild(cardFooter);
    return card
  }


  // Create decline button
  const declineBtn = document.createElement('button');
  declineBtn.className = 'white_button';
  declineBtn.id = 'declineBtn';
  declineBtn.textContent = 'Отклонить';
  declineBtn.style.width = '20%'


  declineBtn.addEventListener('click', function () {
            const loadingIndicator = showLoadingIndicator();
            showNotification('Приглашение отклонено')
            makeRequest({
                method: 'POST',
                url: `/api/responses/${id}/reject`
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

  // Create accept button
  const acceptBtn = document.createElement('button');
  acceptBtn.className = 'red_button';
  acceptBtn.id = 'acceptBtn';
  acceptBtn.textContent = 'Принять';
  acceptBtn.style.width = '20%'

  acceptBtn.addEventListener('click', function () {
            const loadingIndicator = showLoadingIndicator();
            showNotification('Приглашение принято')
            makeRequest({
                method: 'POST',
                url: `/api/responses/${id}/accept`
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

  // Append buttons to footer
  cardFooter.appendChild(declineBtn);
  cardFooter.appendChild(acceptBtn);

  // Assemble the card
  card.appendChild(cardHeader);
  card.appendChild(cardContent);
  card.appendChild(cardFooter);

  return card;
}

window.createInvitationCard = createInvitationCard