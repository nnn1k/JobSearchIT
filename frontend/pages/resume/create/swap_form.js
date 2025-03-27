function nextStep(step) {
    // Скрываем текущий этап
    document.getElementById(`step${step}`).classList.remove('active');
    // Показываем следующий этап
    document.getElementById(`step${step + 1}`).classList.add('active');
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function prevStep(step) {
    // Скрываем текущий этап
    document.getElementById(`step${step}`).classList.remove('active');
    // Показываем предыдущий этап
    document.getElementById(`step${step - 1}`).classList.add('active');
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function addExperience() {
    // Создаем новый элемент опыта
    const newExperienceEntry = document.createElement('div');
    newExperienceEntry.classList.add('experienceEntry');

    newExperienceEntry.innerHTML = `
        <label for="company">Компания:</label>
        <input type="text" class="company" required placeholder="Введите название компании">

        <label for="position">Должность:</label>
        <input type="text" class="position" required placeholder="Введите вашу должность">

        <label for="responsibilities">Обязанности:</label>
        <textarea class="responsibilities" rows="4" required placeholder="Опишите ваши обязанности..."></textarea>

        <label for="startDate">Начало работы:</label>
        <input type="date" class="startDate" required>

        <label for="endDate">Конец работы:</label>
        <input type="date" class="endDate" required>

        <button type="button" onclick="removeExperience(this)">Убрать опыт работы</button>
    `;

    // Добавляем новый элемент в контейнер
    document.getElementById('experienceContainer').appendChild(newExperienceEntry);
}

function removeExperience(button) {
    // Удаляем блок опыта, к которому принадлежит кнопка
    const experienceEntry = button.parentElement;
    experienceEntry.remove();
}

function noExperience() {
    // Удаляем все поля ввода опыта работы
    const experienceContainer = document.getElementById('experienceContainer');
    experienceContainer.innerHTML = '';
}
window.nextStep = nextStep
window.prevStep = prevStep
window.addExperience = addExperience
window.noExperience = noExperience