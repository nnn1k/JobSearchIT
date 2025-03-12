import {makeRequest} from '/frontend/js/utils.js';
import {showNotification} from "/frontend/js/showNotification.js";

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

export function createModal(title, resumes, vacancy_id) {
    document.body.style.overflow = "hidden"
    const modal = document.createElement('div');
    modal.className = 'modal';

    const modalContent = document.createElement('div');
    modalContent.className = 'modal-content';

    const closeButton = document.createElement('span');
    closeButton.className = 'close';
    closeButton.innerHTML = '&times;';

    const modalTitle = document.createElement('h2');
    modalTitle.textContent = title;


    // Создаем контейнер для резюме
    const resumeContainer = document.createElement('div');

    // Добавляем радиокнопки для каждого резюме
    resumes.forEach(resume => {
        console.log('123123')

        const label = document.createElement('label');
        label.textContent = resume.profession.title; // Предполагаем, что у резюме есть поле title

        const radio = document.createElement('input');
        radio.type = 'radio';
        radio.name = 'resume';
        radio.value = resume.id; // Используем id резюме для дальнейших действий

        label.prepend(radio);
        resumeContainer.appendChild(label);
    });

    const userType = getCookie('user_type')

    if (userType === 'worker') {
        const confirmButton = document.createElement('button');
        confirmButton.textContent = 'Откликнуться';
        confirmButton.classList = 'red_button'
        confirmButton.style.position = 'sticky'
        confirmButton.onclick = function () {
            const selectedResume = document.querySelector('input[name="resume"]:checked');
            if (selectedResume) {
                const selectedResumeId = selectedResume.value;
                const searchParams = new URLSearchParams();
                searchParams.append('vacancy_id', vacancy_id)
                searchParams.append('resume_id', selectedResumeId)
                searchParams.append('accept', true)
                const postResponse = makeRequest({
                    method: 'POST',
                    url: `/api/responses/response/?${searchParams.toString()}`,
                })
                if (postResponse) {
                    showNotification('Отправлено')
                    document.body.style.overflow = ""

                }
                modal.style.display = 'none';
                document.body.removeChild(modal);
            } else {
                alert('Пожалуйста, выберите резюме для отклика.');
            }
        };

        modalContent.appendChild(closeButton);
        modalContent.appendChild(modalTitle);
        modalContent.appendChild(resumeContainer);
        modalContent.appendChild(confirmButton);
        modal.appendChild(modalContent);
        document.body.appendChild(modal);
    }

    if (userType === 'employer') {
        const inviteButton = document.createElement('button');
        inviteButton.textContent = 'Пригласить';
        inviteButton.classList = 'red_button'
        inviteButton.style.position = 'sticky'
        inviteButton.onclick = function () {
            const selectedResume = document.querySelector('input[name="resume"]:checked');
            if (selectedResume) {
                const selectedResumeId = selectedResume.value;
                const searchParams = new URLSearchParams();
                searchParams.append('vacancy_id', selectedResumeId)
                searchParams.append('resume_id', vacancy_id)
                searchParams.append('accept', true)
                const postResponse = makeRequest({
                    method: 'POST',
                    url: `/api/responses/invite/?${searchParams.toString()}`,
                })
                if (postResponse) {
                    showNotification('Отправлено')
                    document.body.style.overflow = ""

                }
                modal.style.display = 'none';
                document.body.removeChild(modal);
            } else {
                alert('Пожалуйста, выберите резюме для отклика.');
            }
        };

        modalContent.appendChild(closeButton);
        modalContent.appendChild(modalTitle);
        modalContent.appendChild(resumeContainer);
        modalContent.appendChild(inviteButton);
        modal.appendChild(modalContent);
        document.body.appendChild(modal);
    }


    // Открытие модального окна
    modal.style.display = 'block';

    // Закрытие модального окна при нажатии на "X"
    closeButton.onclick = function () {
        modal.style.display = 'none';
        document.body.removeChild(modal); // Удаляем модальное окно после закрытия
        document.body.style.overflow = ""
    };

    // Закрытие модального окна при нажатии вне его
    window.onclick = function (event) {
        if (event.target === modal) {
            modal.style.display = 'none';
            document.body.removeChild(modal); // Удаляем модальное окно после закрытия
            document.body.style.overflow = ""
        }
    };
}