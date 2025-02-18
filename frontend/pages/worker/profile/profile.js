import {apiUrl, makeRequest} from "/frontend/js/utils.js";
import {hide_field, cancel_btn} from "/frontend/js/functions_for_profile.js";
import {hideLoadingIndicator, showLoadingIndicator} from '/frontend/js/functions_for_loading.js'

document.getElementById('link_for_edit_name').addEventListener('click', function (event) {
    event.preventDefault();
    $(document).ready(function () {
        hide_field('row_by_name', 'row_by_edit_name')
    });
});


$(document).ready(function () {
    cancel_btn('row_by_name', 'row_by_edit_name', 'cancel_btn')
});

document.getElementById('link_for_edit_surname').addEventListener('click', function (event) {
    event.preventDefault();
    $(document).ready(function () {
        hide_field('row_by_surname', 'row_by_edit_surname')
    });
});

$(document).ready(function () {
    cancel_btn('row_by_surname', 'row_by_edit_surname', 'cancel_btn_for_surname')
});

document.getElementById('link_for_edit_patronymic').addEventListener('click', function (event) {
    event.preventDefault();
    $(document).ready(function () {
        hide_field('row_by_patronymic', 'row_by_edit_patronymic')
    });
});

$(document).ready(function () {
    cancel_btn('row_by_patronymic', 'row_by_edit_patronymic', 'cancel_btn_for_patronymic')
});


document.getElementById('link_for_edit_phone').addEventListener('click', function (event) {
    event.preventDefault();
    $(document).ready(function () {
        hide_field('row_by_phone', 'row_by_edit_phone')
    });
});

$(document).ready(function () {
    cancel_btn('row_by_phone', 'row_by_edit_phone', 'cancel_btn_for_phone')
});

document.getElementById('link_for_edit_birthday').addEventListener('click', function (event) {
    event.preventDefault();
    $(document).ready(function () {
        hide_field('row_by_birthday', 'row_by_edit_birthday')
    });
});

$(document).ready(function () {
    cancel_btn('row_by_birthday', 'row_by_edit_birthday', 'cancel_btn_for_birthday')
});

document.getElementById('link_for_edit_city').addEventListener('click', function (event) {
    event.preventDefault();
    $(document).ready(function () {
        hide_field('row_by_city', 'row_by_edit_city')
    });
});


$(document).ready(function () {
    cancel_btn('row_by_city', 'row_by_edit_city', 'cancel_btn_for_city')
});

async function getMe() {
    const loadingIndicator = showLoadingIndicator();
    const getResponse = await makeRequest({
            method: 'GET',
            url: '/api/workers/me',
        }
    )
    const user = getResponse.user
    document.getElementById('data_name').innerHTML = user.name
    document.getElementById('data_name_2').innerHTML = user.name
    document.getElementById('data_surname').innerHTML = user.surname
    document.getElementById('data_surname_2').innerHTML = user.surname
    document.getElementById('data_patronymic').innerHTML = user.patronymic
    document.getElementById('data_patronymic_2').innerHTML = user.patronymic
    document.getElementById('data_email').innerHTML = user.email
    document.getElementById('data_phone').innerHTML = user.phone
    document.getElementById('data_phone_2').innerHTML = user.phone
    document.getElementById('data_birthday').innerHTML = user.birthday
    document.getElementById('data_birthday_2').innerHTML = user.birthday
    document.getElementById('data_city').innerHTML = user.city
    document.getElementById('data_city_2').innerHTML = user.city
    hideLoadingIndicator(loadingIndicator);
}

document.addEventListener("DOMContentLoaded", function () {
    getMe();
})

async function patch_field(field) {
    const loadingIndicator = showLoadingIndicator();
    const value = document.getElementById(`new_${field}`).value
    const patchResponse = await makeRequest({
        method: 'PATCH',
        url: '/api/workers/me',
        data: {
            [field]: value
        }
    })
    location.reload(true);
    hideLoadingIndicator(loadingIndicator);
}

window.patch_field = patch_field
window.hide_field = hide_field
window.cancel_btn = cancel_btn