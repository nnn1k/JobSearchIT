import {apiUrl, makeRequest} from "/frontend/js/utils.js";

document.addEventListener('DOMContentLoaded', function (){
    getSkills()
})

async function getSkills(){
    const getResponse = await makeRequest({
        method: 'GET',
        url: '/api/skills'
    })
}

function nextStep(step) {
    // Скрываем текущий этап
    document.getElementById(`step${step}`).classList.remove('active');
    // Показываем следующий этап
    document.getElementById(`step${step + 1}`).classList.add('active');
}

function prevStep(step) {
    // Скрываем текущий этап
    document.getElementById(`step${step}`).classList.remove('active');
    // Показываем предыдущий этап
    document.getElementById(`step${step - 1}`).classList.add('active');
}

function selectSkill(button) {
    const skillName = button.innerText; // Получаем название навыка
    const selectedSkillsContainer = document.getElementById('selectedSkills');

    // Проверяем, есть ли уже этот навык в выбранных
    if (![...selectedSkillsContainer.children].some(skill => skill.innerText === skillName)) {
        const skillButton = document.createElement('button');
        skillButton.classList.add('selected-skill-button'); // Добавляем класс для стиля
        skillButton.innerText = skillName;

        // Добавляем обработчик события для удаления навыка
        skillButton.onclick = function() {
            selectedSkillsContainer.removeChild(skillButton);
            button.classList.remove('selected'); // Убираем выделение с кнопки
            button.style.display = 'inline-block'; // Показываем кнопку навыка снова
        };

        selectedSkillsContainer.appendChild(skillButton);

        // Выделяем кнопку и скрываем ее из доступных навыков
        button.classList.add('selected');
        button.style.display = 'none'; // Скрываем кнопку навыка
    }
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

async function postResume(){
    const title = document.getElementById('title').value
    const description = document.getElementById('description').value
    const salary_first = Number(document.getElementById('salary_first').value)
    const salary_second = Number(document.getElementById('salary_second').value)
    const city = document.getElementById('city').value
    const postResponse = await makeRequest({
        method: 'POST',
        url: '/api/resumes/',
        data: {
            title,
            description,
            salary_first,
            salary_second,
            city
        }
    })
    if (postResponse.status) {
        alert('Вакансия добавлена')
        window.location.href = apiUrl + '/worker/profile'
    }
}
function submitResume(event) {
    event.preventDefault(); // Предотвращаем обновление страницы
    postResume()
}

function createSkillButtons(skillList) {
        const skillsContainer = document.getElementById('skillsContainer');

        // Очищаем контейнер перед добавлением новых кнопок (если нужно)
        skillsContainer.innerHTML = '';

        // Перебираем список навыков и создаем кнопки
        skillList.forEach(skill => {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'skill-button';
            button.textContent = skill;
            button.onclick = function() { selectSkill(this); }; // Привязываем событие onclick
            skillsContainer.appendChild(button); // Добавляем кнопку в контейнер
        });
    }

window.submitResume = submitResume
window.nextStep = nextStep
window.prevStep = prevStep