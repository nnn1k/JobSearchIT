import {apiUrl, makeRequest} from "/frontend/js/utils.js";
import {hideLoadingIndicator, showLoadingIndicator} from '/frontend/js/functions_for_loading.js'


var profession_id

tinymce.init({
    menubar: false,
    statusbar: false,
    display: "flex",
    selector: '#input_for_description_vacancy',
    width: 600,
    height: 500,
    fontsize: 50,
    whiteSpace: "pre-wrap"
});
document.addEventListener('DOMContentLoaded', function (){
    get_vacancy()
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

    const availableJobs = getResponse.professions



    // Function to filter and show matching jobs
    const filterJobs = (searchText) => {
        jobsDropdown.innerHTML = '';
        if (!searchText) {
            jobsDropdown.style.display = 'none';
            return;
        }

        const matchingJobs = availableJobs.filter(job =>
            job.title.toLowerCase().includes(searchText.toLowerCase())
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
                jobInput.value = job.title;
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

async function get_vacancy() {
    const vacancyId = location.pathname.split('/')[2]
    const loadingIndicator = showLoadingIndicator();
    const getResponse = await makeRequest({
        method: 'GET',
        url: `/api/vacancy/${vacancyId}`
    })
    console.log(getResponse)
    if (getResponse) {
        profession_id = getResponse.vacancy.profession.id
        console.log(profession_id)
        const vacancy = getResponse.vacancy;
        const skills = getResponse.vacancy.skills;
        document.getElementById('jobInput').value = vacancy.profession.title
        document.getElementById('input_for_city_vacancy').value = vacancy.city;
        tinymce.get('input_for_description_vacancy').setContent(vacancy.description)
        document.getElementById('input_for_first_salary').value = vacancy.salary_first
        document.getElementById('input_for_second_salary').value = vacancy.salary_second
        console.log(skills)
        const displaySkills = () => {
            const skillsDisplay = document.getElementById('skillsList');
            skillsDisplay.value = '';

            if (skills.length === 0) {
                const link = document.createElement('a');
                link.textContent = 'Добавить навыки';
                link.href = `/vacancies/${vacancyId}/edit/skills`;
                link.classList.add('resume-link');
                skillsDisplay.appendChild(link)
                return;
            }
            skills.forEach(skill => {
                const skillTag = document.createElement('div');
                skillTag.className = 'skill-tag';
                console.log(skill.name)
                skillTag.textContent = skill.name;
                skillsDisplay.appendChild(skillTag);
            });
            const linkForEditSkills = document.createElement('a');
            linkForEditSkills.href = `/vacancies/${vacancyId}/edit/skills`;
            linkForEditSkills.classList.add('resume-link');
            linkForEditSkills.textContent = 'Изменить';
            skillsDisplay.appendChild(linkForEditSkills);
            };
        displaySkills();
        hideLoadingIndicator(loadingIndicator);
    }
}


async function put_vacancy(){
    const vacancyId = location.pathname.split('/')[2]
    const loadingIndicator = showLoadingIndicator();
    const description = tinymce.get('input_for_description_vacancy').getContent()
    const city = document.getElementById('input_for_city_vacancy').value
    const salary_first = document.getElementById('input_for_first_salary').value
    const salary_second = document.getElementById('input_for_second_salary').value
    const putResponse = await makeRequest({
        method: 'PUT',
        url: `/api/vacancy/${vacancyId}`,
        data: {
            profession_id,
            description,
            city,
            salary_first,
            salary_second,
        }
    })
    window.location.href = apiUrl + `/vacancies/${vacancyId}`
}
window.put_vacancy = put_vacancy