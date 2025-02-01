import {apiUrl, makeRequest} from "/frontend/js/utils.js";

document.addEventListener('DOMContentLoaded', function (){
    getSkills()
})

async function getSkills(){
    const getResponse = await makeRequest({
        method: 'GET',
        url: '/api/skills/'
    })
    const skills = getResponse.skills
    createSkillButtons(skills)
}

async function postResume(){
    const title = document.getElementById('title').value
    const description = document.getElementById('description').value
    const salary_first = Number(document.getElementById('salary_first').value)
    const salary_second = Number(document.getElementById('salary_second').value)
    const city = document.getElementById('city').value
    const skills = getSelectedSkills()
    const postResponse = await makeRequest({
        method: 'POST',
        url: '/api/resumes/',
        data: {
            title,
            description,
            salary_first,
            salary_second,
            city,
            skills
        }
    })
    if (postResponse.status) {
        alert('Резюме добавлена')
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
        button.textContent = skill.name; // Используем name для текста кнопки
        button.setAttribute('data-id', skill.id); // Сохраняем id в атрибуте data-id
        button.onclick = function() { selectSkill(this); }; // Привязываем событие onclick
        skillsContainer.appendChild(button); // Добавляем кнопку в контейнер
    });
}
function getSelectedSkills() {
    const selectedSkillsContainer = document.getElementById('selectedSkills');
    const selectedSkills = [...selectedSkillsContainer.children].map(skillButton => {
        return {
            id: Number(skillButton.getAttribute('data-id')), // Получаем id из атрибута data-id
            name: skillButton.innerText // Используем текст кнопки как name
        };
    });
    return selectedSkills;
}

function selectSkill(button) {
    const skillName = button.innerText; // Получаем название навыка
    const selectedSkillsContainer = document.getElementById('selectedSkills');

    // Проверяем, есть ли уже этот навык в выбранных
    if (![...selectedSkillsContainer.children].some(skill => skill.innerText === skillName)) {
        const skillButton = document.createElement('button');
        skillButton.classList.add('selected-skill-button'); // Добавляем класс для стиля
        skillButton.innerText = skillName;
        skillButton.setAttribute('data-id', button.getAttribute('data-id')); // Сохраняем id

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

    console.log(getSelectedSkills());
}

window.submitResume = submitResume
