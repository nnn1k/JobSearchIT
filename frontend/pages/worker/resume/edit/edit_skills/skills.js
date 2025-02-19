import {apiUrl, makeRequest} from "/frontend/js/utils.js";
import {hideLoadingIndicator, showLoadingIndicator} from '/frontend/js/functions_for_loading.js'

var skills = [];

document.addEventListener('DOMContentLoaded', function () {
    getSkills()
})


async function getSkills() {
    const resume_id = location.pathname.split('/')[3]
    const loadingIndicator = showLoadingIndicator();
    const getResponse = await makeRequest({
        method: 'GET',
        url: `/api/skills/resumes/${resume_id}`
    })
    hideLoadingIndicator(loadingIndicator)
    const available_skills = getResponse.available_skills;
    const select_skills = getResponse.resume_skills;
    skills = select_skills
    const skillInput = document.getElementById('skillInput');
    const skillsList = document.getElementById('skillsList');
    const skillsDropdown = document.getElementById('skillsDropdown');

    const sk = available_skills.sort((a, b) => a.name.localeCompare(b.name));


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
                skills.splice(index, 1); // Удаление навыка из списка
                tag.remove();
            }
        });

        return tag;
    };

    skills.forEach(skill => {
        skillsList.appendChild(createSkillTag(skill));
    });

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
                if (!skills.some(s => s.id === skill.id)) {
                    skills.push(skill)
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

async function put_skills(){
    const resume_id = location.pathname.split('/')[3]
    const loadingIndicator = showLoadingIndicator();
    const putResponse = await makeRequest({
        method: 'PUT',
        url: `/api/skills/resumes/${resume_id}`,
        data: {
            skills
        }
    })
    window.location.href = apiUrl + `/worker/resumes/${resume_id}/edit/`
}

async function cancel_click() {
    const resume_id = location.pathname.split('/')[3]
    window.location.href = apiUrl + `/worker/resumes/${resume_id}/edit/`
}

window.cancel_click = cancel_click
window.put_skills = put_skills