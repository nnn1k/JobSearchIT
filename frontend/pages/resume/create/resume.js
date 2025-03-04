import {apiUrl, makeRequest} from "/frontend/js/utils.js";


const skills = [];

var profession_id = 1

document.addEventListener('DOMContentLoaded', function () {
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
    getProfessions()
})


async function getProfessions() {

    const getResponse = await makeRequest({
        method: 'GET',
        url: '/api/professions'
    })
    const form = document.getElementById('jobForm');
    const jobInput = document.getElementById('jobInput');
    const jobsDropdown = document.getElementById('jobsDropdown');
    const nextButton = document.getElementById('next_after_title');

    // Имитация списка IT профессий с сервера в виде объектов
    const availableJobs = getResponse.professions


    // const availableJobs = noSortAvailableJobs.sort((a, b) => a.name.localeCompare(b.name));

    // Function to filter and show matching jobs
    const filterJobs = (searchText) => {
        jobsDropdown.innerHTML = '';
        if (!searchText) {
            jobsDropdown.style.display = 'none';
            return;
        }

        const matchingJobs = availableJobs.filter(job =>
            job.title.toLowerCase().startsWith(searchText.toLowerCase())
        );

        if (matchingJobs.length === 0) {
            jobsDropdown.style.display = 'none';
            return;
        }

        matchingJobs.forEach(job => {
            const option = document.createElement('div');
            option.className = 'job-option';
            option.textContent = job.title;
            option.addEventListener('click', () => {
                profession_id = job.id
                jobInput.value = job.title; // Вставка выбранной профессии в input
                jobsDropdown.style.display = 'none';
            });
            jobsDropdown.appendChild(option);
        });

        jobsDropdown.style.display = 'block';
    };

    // Event listener for input changes
    jobInput.addEventListener('input', (e) => {
        filterJobs(e.target.value);
    });

    // Hide dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!jobInput.contains(e.target) && !jobsDropdown.contains(e.target)) {
            jobsDropdown.style.display = 'none';
        }
    });
}


async function getSkills() {
    const getResponse = await makeRequest({
        method: 'GET',
        url: '/api/skills/'
    })
    const available_skills = getResponse.skills
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
                    skills.push(skill);
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

async function postResume() {
    const description = tinymce.get('description').getContent()
    const salary_first = Number(document.getElementById('salary_first').value)
    const salary_second = Number(document.getElementById('salary_second').value)
    const city = document.getElementById('city').value
    const postResponse = await makeRequest({
        method: 'POST',
        url: '/api/workers/resumes/',
        data: {
            profession_id,
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
