import {hideLoadingIndicator, showLoadingIndicator} from '/frontend/js/functions_for_loading.js'
import {apiUrl, makeRequest} from '/frontend/js/utils.js';
import {formatDateTime} from "/frontend/js/timefunc.js";
import {showNotification} from "/frontend/js/showNotification.js";
import {createInvitationCard} from "./createInvitationsForWorker.js";
import {createInviteForEmployer} from "./createInvitationsForEmployer.js";

document.addEventListener('DOMContentLoaded', function () {
    const first_button = document.getElementById('switch_all')
    showForm('all_form', first_button)
    getInvitations()
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

    const buttons = document.querySelectorAll('.btns')
    buttons.forEach(btn => {
        btn.classList.remove('active')
    })
    button.classList.add('active');
}


async function getInvitations() {
    const loadingIndicator = showLoadingIndicator();
    const getResponse = await makeRequest({
        method: 'GET',
        url: `/api/responses/invite`
    })

    const userType = getCookie('user_type')

    if (userType === 'worker') {
        renderInvitationsForWorker(getResponse.all, 'all_form')
        renderInvitationsForWorker(getResponse.waiting, 'unread_form')
        renderInvitationsForWorker(getResponse.accepted, 'invites_form')
        renderInvitationsForWorker(getResponse.rejected, 'discard_form')
    }
    if (userType === 'employer') {
        renderInvitationsForEmployer(getResponse.all, 'all_form')
        renderInvitationsForEmployer(getResponse.waiting, 'unread_form')
        renderInvitationsForEmployer(getResponse.accepted, 'invites_form')
        renderInvitationsForEmployer(getResponse.rejected, 'discard_form')
    }

    console.log(getResponse)
    hideLoadingIndicator(loadingIndicator)
}

function renderInvitationsForWorker(invitations, nameForm){
    const invitations_form = document.getElementById(nameForm)
    invitations_form.innerHTML = '';
    if (invitations.length === 0) {
        const countInvitations = document.createElement('h2');
        countInvitations.textContent = `Тут пока пусто :(`
        invitations_form.appendChild(countInvitations);
        return
    }

    invitations.forEach(invate => {
        const card = createInvitationCard(invate.vacancy.company.name, invate.vacancy.profession.title,
            formatDateTime(invate.created_at), invate.resume.profession.title, invate.is_employer_accepted, invate.is_worker_accepted,
            invate.id, invate.chat.id)
        invitations_form.appendChild(card)
    })
}

function renderInvitationsForEmployer(invitations, nameForm){
    const invitations_form = document.getElementById(nameForm)
    invitations_form.innerHTML = '';
    if (invitations.length === 0) {
        const countInvitations = document.createElement('h2');
        countInvitations.textContent = `Тут пока пусто :(`
        invitations_form.appendChild(countInvitations);
        return
    }

    invitations.forEach(invate => {
        const card = createInviteForEmployer(invate)
        invitations_form.appendChild(card)
    })
}

window.showForm = showForm