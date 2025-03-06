import {hideLoadingIndicator, showLoadingIndicator} from '/frontend/js/functions_for_loading.js'
import {apiUrl, makeRequest} from '/frontend/js/utils.js';
import {formatDateTime} from "/frontend/js/timefunc.js";

document.addEventListener('DOMContentLoaded', function () {
    const first_button = document.getElementById('switch_all')
    showForm('all_form', first_button)
    getFeedbacks()
})


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

async function getFeedbacks(){
    const loadingIndicator = showLoadingIndicator();
    const getResponse = await makeRequest({
        method: 'GET',
        url: `/api/responses/response`
    })
    console.log(getResponse)
    renderFeedbacks(getResponse.all, getResponse.accepted, getResponse.rejected, getResponse.waiting)
    hideLoadingIndicator(loadingIndicator)
}


function renderFeedbacks(allFeedbacks, acceptedFeedback, rejectedFeedback, waitingFeedback){
    const all_feedbacks = document.getElementById('all_form')
    all_feedbacks.innerHTML = '';
    if (allFeedbacks.length === 0){
        const countFeedbacks = document.createElement('h2');
        countFeedbacks.textContent = `Тут пока пусто :(`
        all_feedbacks.appendChild(countFeedbacks);
    }
    allFeedbacks.forEach(vacancy => {
        const feedbackElement = document.createElement('div');
        feedbackElement.classList = 'feedback'

        const titleVacancy = document.createElement('h2');
        titleVacancy.textContent = vacancy.vacancy_id
        const nameCompany = document.createElement('h3');
        nameCompany.textContent = 'Название компании(которого блять нет)'
        const createAt = document.createElement('p')
        createAt.textContent = formatDateTime(vacancy.created_at)
        const deleteBtn = document.createElement('button')
        deleteBtn.textContent = 'Удалить'
        deleteBtn.classList = 'red_button'
        deleteBtn.style.marginLeft = '70%'
        deleteBtn.style.width = '25%'
        feedbackElement.appendChild(titleVacancy)
        feedbackElement.appendChild(nameCompany)
        feedbackElement.appendChild(createAt)
        feedbackElement.appendChild(deleteBtn)
        all_feedbacks.appendChild(feedbackElement)
    });

    const accepted_feedbacks = document.getElementById('invites_form')
    accepted_feedbacks.innerHTML = ''
    if (acceptedFeedback.length === 0){
        const countFeedbacks = document.createElement('h2');
        countFeedbacks.textContent = `Тут пока пусто :(`
        accepted_feedbacks.appendChild(countFeedbacks);
    }
    acceptedFeedback.forEach(vacancy => {
        const feedbackElement = document.createElement('div');
        feedbackElement.classList = 'feedback'

        const titleVacancy = document.createElement('h2');
        titleVacancy.textContent = vacancy.vacancy_id
        const nameCompany = document.createElement('h3');
        nameCompany.textContent = 'Название компании(которого блять нет)'
        const createAt = document.createElement('p')
        createAt.textContent = formatDateTime(vacancy.created_at)
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
    if (rejectedFeedback.length === 0){
        const countFeedbacks = document.createElement('h2');
        countFeedbacks.textContent = `Тут пока пусто :(`
        rejected_feedbacks.appendChild(countFeedbacks);
    }
    rejectedFeedback.forEach(vacancy => {
        const feedbackElement = document.createElement('div');
        feedbackElement.classList = 'feedback'

        const titleVacancy = document.createElement('h2');
        titleVacancy.textContent = vacancy.vacancy_id
        const nameCompany = document.createElement('h3');
        nameCompany.textContent = 'Название компании(которого блять нет)'
        const createAt = document.createElement('p')
        createAt.textContent = formatDateTime(vacancy.created_at)
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
    if (waitingFeedback.length === 0){
        const countFeedbacks = document.createElement('h2');
        countFeedbacks.textContent = `Тут пока пусто :(`
        waiting_feedbacks.appendChild(countFeedbacks);
    }
    waitingFeedback.forEach(vacancy => {
        const feedbackElement = document.createElement('div');
        feedbackElement.classList = 'feedback'

        const titleVacancy = document.createElement('h2');
        titleVacancy.textContent = vacancy.vacancy_id
        const nameCompany = document.createElement('h3');
        nameCompany.textContent = 'Название компании(которого блять нет)'
        const createAt = document.createElement('p')
        createAt.textContent = formatDateTime(vacancy.created_at)
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


window.showForm = showForm