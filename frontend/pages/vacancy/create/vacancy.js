import {apiUrl, makeRequest} from '/frontend/js/utils.js';

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


async function post_vacancy() {
    const title = document.getElementById('input_for_title_vacancy').value
    const description = document.getElementById('input_for_description_vacancy').value
    const salary_first = Number(document.getElementById('input_for_first_salary').value)
    const salary_second = Number(document.getElementById('input_for_second_salary').value)
    const city = document.getElementById('input_for_city_vacancy').value
    if (!title){
        alert('Не все данные заполнены')
        return
    }

    const postResponse = await makeRequest({
        method: 'POST',
        url: '/api/vacancy',
        data: {
            title,
            description,
            salary_first,
            salary_second,
            city
        }
    })
    if (postResponse) {
        window.location.href = apiUrl + "/vacancies/add"
        alert('Вакансия опубликована');
    }


}

window.post_vacancy = post_vacancy