const resumes = [
    {
        id: 1,
        title: "Frontend Developer",
        salary_first: "100 000",
        salary_second: "", // Вторая зарплата не указана
        city: "Москва",
        description: "Опыт работы с React и Vue.js. Участие в крупных проектах.",
    },
    {
        id: 2,
        title: "Backend Developer",
        salary_first: "", // Первая зарплата не указана
        salary_second: "110 000",
        city: "Санкт-Петербург",
        description: "Знания Python и Django. Опыт работы с RESTful API.",
    },
    {
        id: 3,
        title: "UI/UX Designer",
        salary_first: "", // Обе зарплаты не указаны
        salary_second: "",
        city: "Казань",
        description: "Опыт работы с Figma и Adobe XD. Создание прототипов.",
    },
];

const container = document.getElementById('resume-container');

resumes.forEach(resume => {
    const resumeElement = document.createElement('div');
    resumeElement.classList.add('resume');

    const titleElement = document.createElement('h2');
    titleElement.textContent = resume.title;

    const salaryElement = document.createElement('p');
    if (resume.salary_first) {
        salaryElement.innerHTML = `<strong>Зарплата:</strong> от ${resume.salary_first} ₽`;
    } else if (resume.salary_second) {
        salaryElement.innerHTML = `<strong>Зарплата:</strong> до ${resume.salary_second} ₽`;
    } else {
        salaryElement.innerHTML = `<strong>Зарплата:</strong> не указана`;
    }

    const cityElement = document.createElement('p');
    cityElement.innerHTML = `<strong>Город:</strong> ${resume.city}`;

    const descriptionElement = document.createElement('p');
    descriptionElement.classList.add('description'); // Применяем новый стиль
    descriptionElement.innerHTML = `<strong>Описание:</strong> ${resume.description}`;

    const editButton = document.createElement('button');
    editButton.classList.add('edit-button');
    editButton.textContent = "Редактировать";
    // Обработчик перенаправления на страницу редактирования резюме
    editButton.onclick = () => {
        window.location.href = `/resumes/${resume.id}/edit`;
    };

    resumeElement.appendChild(titleElement);
    resumeElement.appendChild(salaryElement);
    resumeElement.appendChild(cityElement);
    resumeElement.appendChild(descriptionElement);
    resumeElement.appendChild(editButton); // Добавляем кнопку редактирования

    container.appendChild(resumeElement);
});