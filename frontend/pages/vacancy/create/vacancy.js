import {apiUrl, makeRequest} from '/frontend/js/utils.js';
import {hideLoadingIndicator, showLoadingIndicator} from '/frontend/js/functions_for_loading.js'

const skills = [];

tinymce.init({
    menubar: false,
    statusbar: false,
    selector: '#input_for_description_vacancy',
    width: 500,  // Фиксированная ширина
    height: 500, // Фиксированная высота
});
document.addEventListener('DOMContentLoaded', () => {
    getSkills()
})

async function getSkills() {
    const getResponse = await makeRequest({
        method: 'GET',
        url: '/api/skills/'
    })
    const available_skills = getResponse.skills;
    const skillInput = document.getElementById('skillInput');
    const skillsDropdown = document.getElementById('skillsDropdown');

    const sk = available_skills.sort((a, b) => a.name.localeCompare(b.name));

    // Function to create a skill tag
    const createSkillTag = (skill) => {
        const tag = document.createElement('div');
        tag.className = 'skill-tag';
        tag.innerHTML = `
      ${skill.name}
      <button type="button" aria-label="Удалить навык">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M18 6 6 18"/>
          <path d="m6 6 12 12"/>
        </svg>
      </button>
    `;

        tag.querySelector('button').addEventListener('click', () => {
            const index = skills.findIndex(s => s.id === skill.id);
            if (index !== -1) {
                skills.splice(index, 1);
                tag.remove();
            }
        });
        return tag;
    };

    // Function to filter and show matching skills
    const filterSkills = (searchText) => {
        skillsDropdown.innerHTML = '';
        if (!searchText) {
            skillsDropdown.style.display = 'none';
            return;
        }

        const matchingSkills = sk.filter(skill =>
            skill.name.toLowerCase().includes(searchText.toLowerCase()) &&
            !skills.some(s => s.id === skill.id)
        );

        if (matchingSkills.length === 0) {
            skillsDropdown.style.display = 'none';
            return;
        }

        matchingSkills.forEach(skill => {
            const option = document.createElement('div');
            option.className = 'skill-option';
            option.textContent = skill.name;
            option.addEventListener('click', () => {
                if (!skills.some(s => s.id === skill.id)) { // Проверка наличия навыка
                    skills.push(skill); // Добавление навыка в список
                    skillsList.appendChild(createSkillTag(skill));
                    skillInput.value = '';
                    skillsDropdown.style.display = 'none';
                }
            });
            skillsDropdown.appendChild(option);
        });

        skillsDropdown.style.display = 'block';
    };

    // Event listener for input changes
    skillInput.addEventListener('input', (e) => {
        filterSkills(e.target.value);
    });

    // Hide dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!skillInput.contains(e.target) && !skillsDropdown.contains(e.target)) {
            skillsDropdown.style.display = 'none';
        }
    });
}

async function post_vacancy() {
    const title = document.getElementById('input_for_title_vacancy').value
    const description = tinymce.get('input_for_description_vacancy').getContent()
    const salary_first = Number(document.getElementById('input_for_first_salary').value)
    const salary_second = Number(document.getElementById('input_for_second_salary').value)
    const city = document.getElementById('input_for_city_vacancy').value
    if (!title) {
        alert('Не все данные заполнены')
        return
    }
    const postBtn = document.getElementById('add_vacancy_btn')
    postBtn.disabled = true
    const loadingIndicator = showLoadingIndicator();
    const postResponse = await makeRequest({
        method: 'POST',
        url: '/api/vacancy',
        data: {
            title,
            description,
            salary_first,
            salary_second,
            city,
            skills
        }
    })
    if (postResponse) {
        postBtn.disabled = false
        hideLoadingIndicator(loadingIndicator);
        window.location.href = apiUrl + "/vacancies/add"
        alert('Вакансия опубликована');
    }
    postBtn.disabled = false
    hideLoadingIndicator(loadingIndicator);
}

window.post_vacancy = post_vacancy