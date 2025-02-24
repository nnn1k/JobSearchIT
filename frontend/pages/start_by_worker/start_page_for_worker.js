import {apiUrl} from '/frontend/js/utils.js';

document.querySelector('.search-form').addEventListener('submit', function (event) {
    event.preventDefault(); // Предотвращаем стандартное поведение формы

    const searchInput = document.getElementById('job-search').value; // Получаем значение из поля ввода
    const searchParams = new URLSearchParams({profession: searchInput});
    const searchUrl = apiUrl + `/vacancies/?${searchParams.toString()}`;

    window.location.href = searchUrl;
});