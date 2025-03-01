import {apiUrl, makeRequest} from "/frontend/js/utils.js";
import {hideLoadingIndicator, showLoadingIndicator} from '/frontend/js/functions_for_loading.js'

$(document).ready(function () {
        let currentStep = 0;
        const steps = $('.step');

        // Функция для показа текущего шага
        function showStep(step) {
            steps.removeClass('active').hide(); // Скрываем все шаги
            $(steps[step]).addClass('active').fadeIn(); // Показываем текущий шаг
        }

        // Показать первый шаг
        showStep(currentStep);

        // Переход на следующий шаг
        $('#next1').click(function () {
            currentStep++;
            showStep(currentStep);
        });

        $('#next2').click(function () {
            currentStep++;
            showStep(currentStep);
        });

        $('#next3').click(function () {
            currentStep++;
            showStep(currentStep);
        });

        // Переход на предыдущий шаг
        $('#prev1').click(function () {
            currentStep--;
            showStep(currentStep);
        });

        $('#prev2').click(function () {
            currentStep--;
            showStep(currentStep);
        });

        $('#prev3').click(function () {
            currentStep--;
            showStep(currentStep);
        });
    });


async function insert_data_for_profile() {
    const surname = document.getElementById("surname").value
    const name = document.getElementById("name").value
    const patronymic = document.getElementById("patronymic").value
    const phone = document.getElementById("phone").value
    const completeBtn = document.getElementById('complete_reg')
    completeBtn.disabled = true
    const loadingIndicator = showLoadingIndicator();
    const putResponse = await makeRequest({
        method: 'PUT',
        url: '/api/employers/me',
        data: {
            surname,
            name,
            patronymic,
            phone
        }
    })
    if (putResponse){
        hideLoadingIndicator(loadingIndicator);
        completeBtn.disabled = false
        window.location.href=apiUrl+"/employer/profile"
    }
}

window.insert_data_for_profile = insert_data_for_profile