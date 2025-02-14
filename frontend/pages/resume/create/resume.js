import {apiUrl, makeRequest} from "/frontend/js/utils.js";

const skills = [];

document.addEventListener('DOMContentLoaded', function (){
    tinymce.init({
        menubar: false,
        statusbar: false,
        display: "flex",
        selector: '#description',
        width: 500,
        height: 400,
        fontsize: 50,
        whiteSpace: "pre-wrap"
    });
    getSkills()

})

async function getSkills(){
    const getResponse = await makeRequest({
        method: 'GET',
        url: '/api/skills/worker/me'
    })
    const available_skills = getResponse.available_skills
    const skillInput = document.getElementById('skillInput');
    const skillsList = document.getElementById('skillsList');
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
        skills.splice(index, 1); // Удаление навыка из списка
        console.log(skills);
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

async function postResume(){
    const title = document.getElementById('title').value
    const description = tinymce.get('description').getContent()
    const salary_first = Number(document.getElementById('salary_first').value)
    const salary_second = Number(document.getElementById('salary_second').value)
    const city = document.getElementById('city').value
    const postResponse = await makeRequest({
        method: 'POST',
        url: '/api/workers/resumes/',
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
        alert('Резюме добавлено')
        window.location.href = apiUrl + '/worker/profile'
    }
}

function submitResume(event) {
    event.preventDefault(); // Предотвращаем обновление страницы
    postResume()
}


window.submitResume = submitResume
