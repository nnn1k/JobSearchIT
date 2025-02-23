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
    get_resume()
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

async function get_resume(){
    const resume_id = location.pathname.split('/')[3]
    const loadingIndicator = showLoadingIndicator();
    const getResponse = await makeRequest({
        method: 'GET',
        url: `/api/workers/resumes/${resume_id}`
    })
    hideLoadingIndicator(loadingIndicator);
    profession_id = getResponse.resume.profession_id
    const resume= getResponse.resume
    const skills = getResponse.resume.skills
    console.log(profession_id)
    document.getElementById('jobInput').value = resume.profession.title;
    document.getElementById('input_for_city_vacancy').value = resume.city
    tinymce.get('input_for_description_vacancy').setContent(resume.description)
    document.getElementById('input_for_first_salary').value = resume.salary_first
    document.getElementById('input_for_second_salary').value = resume.salary_second
    const displaySkills = () => {
            const skillsDisplay = document.getElementById('skillsList');
            skillsDisplay.innerHTML = '';

            if (skills.length === 0) {
                const link = document.createElement('a');
                link.textContent = 'Добавить навыки';
                link.href = `/worker/resumes/${resume_id}/edit/skills`;
                link.classList.add('resume-link');
                skillsDisplay.appendChild(link)
                return;
            }
            skills.forEach(skill => {
                const skillTag = document.createElement('div');
                skillTag.className = 'skill-tag';
                skillTag.textContent = skill.name;
                skillsDisplay.appendChild(skillTag);
            });
            const linkForEditSkills = document.createElement('a');
            linkForEditSkills.href = `/worker/resumes/${resume_id}/edit/skills`;
            linkForEditSkills.classList.add('resume-link');
            linkForEditSkills.textContent = 'Изменить';
            skillsDisplay.appendChild(linkForEditSkills);
            };
        displaySkills();
}


async function put_resume(){
    const resume_id = location.pathname.split('/')[3]
    const loadingIndicator = showLoadingIndicator();
    // const title = document.getElementById('jobInput').value
    console.log(profession_id)
    const description = tinymce.get('input_for_description_vacancy').getContent()
    const city = document.getElementById('input_for_city_vacancy').value
    const salary_first = document.getElementById('input_for_first_salary').value
    const salary_second = document.getElementById('input_for_second_salary').value
    const putResponse = await makeRequest({
        method: 'PUT',
        url: `/api/workers/resumes/${resume_id}`,
        data: {
            profession_id,
            description,
            city,
            salary_first,
            salary_second,
        }
    })
    window.location.href = apiUrl + `/resumes/${resume_id}`
}
window.put_resume = put_resume