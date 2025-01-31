function nextStep(step) {
    // Скрываем текущий этап
    document.getElementById(`step${step}`).classList.remove('active');
    // Показываем следующий этап
    document.getElementById(`step${step + 1}`).classList.add('active');
}

function prevStep(step) {
    // Скрываем текущий этап
    document.getElementById(`step${step}`).classList.remove('active');
}