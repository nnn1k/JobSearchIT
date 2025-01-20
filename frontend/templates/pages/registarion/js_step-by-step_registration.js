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


