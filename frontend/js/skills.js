export function createSkillButtons(skillList) {
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
        button.onclick = function () {
            selectSkill(this);
        }; // Привязываем событие onclick
        skillsContainer.appendChild(button); // Добавляем кнопку в контейнер
    });
}

export function getSelectedSkills() {
    const selectedSkillsContainer = document.getElementById('selectedSkills');
    const selectedSkills = [...selectedSkillsContainer.children].map(skillButton => {
        return {
            id: Number(skillButton.getAttribute('data-id')), // Получаем id из атрибута data-id
            name: skillButton.innerText // Используем текст кнопки как name
        };
    });
    return selectedSkills;
}

export function selectSkill(button) {
    const skillName = button.innerText; // Получаем название навыка
    const selectedSkillsContainer = document.getElementById('selectedSkills');

    // Проверяем, есть ли уже этот навык в выбранных
    if (![...selectedSkillsContainer.children].some(skill => skill.innerText === skillName)) {
        const skillButton = document.createElement('button');
        skillButton.classList.add('selected-skill-button'); // Добавляем класс для стиля
        skillButton.innerText = skillName;
        skillButton.setAttribute('data-id', button.getAttribute('data-id')); // Сохраняем id

        // Добавляем обработчик события для удаления навыка
        skillButton.onclick = function () {
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

export function displaySelectedSkills(skills, disabled = false) {
    const selectedSkillsContainer = document.getElementById('selectedSkills');

    // Очищаем контейнер перед добавлением новых выбранных навыков
    selectedSkillsContainer.innerHTML = '';

    // Перебираем массив навыков и создаем кнопки для выбранных
    skills.forEach(skill => {
        const skillButton = document.createElement('button');
        skillButton.classList.add('selected-skill-button'); // Добавляем класс для стиля
        skillButton.innerText = skill.name; // Используем название навыка
        skillButton.setAttribute('data-id', skill.id); // Сохраняем id в атрибуте data-id

        // Добавляем обработчик события для удаления навыка
        if (!disabled) {
            skillButton.onclick = function () {
                selectedSkillsContainer.removeChild(skillButton);
                // Возвращаем кнопку навыка обратно в доступные навыки
                const allSkillButtons = document.querySelectorAll('.skill-button');
                const skillButtonToShow = Array.from(allSkillButtons).find(btn => btn.getAttribute('data-id') === skill.id.toString());
                if (skillButtonToShow) {
                    skillButtonToShow.classList.remove('selected'); // Убираем выделение с кнопки
                    skillButtonToShow.style.display = 'inline-block'; // Показываем кнопку навыка снова
                }
            };
        }
        selectedSkillsContainer.appendChild(skillButton);
    });
}