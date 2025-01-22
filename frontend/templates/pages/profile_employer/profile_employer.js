import {apiUrl, makeRequest} from "../../../js/utils.js";
import {hide_feild, cancel_btn} from "../../../js/functions_for_profile.js";


document.getElementById('link_for_edit_name').addEventListener('click', function (event) {
    event.preventDefault();
    $(document).ready(function () {
        hide_feild('row_by_name', 'row_by_edit_name')
    });
});


$(document).ready(function () {
    cancel_btn('row_by_name', 'row_by_edit_name', 'cancel_btn')
});

document.getElementById('link_for_edit_surname').addEventListener('click', function (event) {
    event.preventDefault();
    $(document).ready(function () {
        hide_feild('row_by_surname', 'row_by_edit_surname')
    });
});

$(document).ready(function () {
    cancel_btn('row_by_surname', 'row_by_edit_surname', 'cancel_btn_for_surname')
});

document.getElementById('link_for_edit_patronymic').addEventListener('click', function (event) {
    event.preventDefault();
    $(document).ready(function () {
        hide_feild('row_by_patronymic', 'row_by_edit_patronymic')
    });
});

$(document).ready(function () {
    cancel_btn('row_by_patronymic', 'row_by_edit_patronymic', 'cancel_btn_for_patronymic')
});


document.getElementById('link_for_edit_phone').addEventListener('click', function (event) {
    event.preventDefault();
    $(document).ready(function () {
        hide_feild('row_by_phone', 'row_by_edit_phone')
    });
});

$(document).ready(function () {
    cancel_btn('row_by_phone', 'row_by_edit_phone', 'cancel_btn_for_phone')
});

document.getElementById('link_for_edit_company').addEventListener('click', function (event) {
    event.preventDefault();
    $(document).ready(function () {
        hide_feild('row_by_сompany', 'row_by_edit_сompany')
    });
});

$(document).ready(function () {
    cancel_btn('row_by_сompany', 'row_by_edit_сompany', 'cancel_btn_for_сompany')
});

async function getMe() {
    const getResponse = await makeRequest({
            method: 'GET',
            url: '/api/employers/me',
        }
    )
    console.log(getResponse)
    document.getElementById('data_name').innerHTML = getResponse.employer.name
    document.getElementById('data_name_2').innerHTML = getResponse.employer.name
    document.getElementById('data_surname').innerHTML = getResponse.employer.surname
    document.getElementById('data_surname_2').innerHTML = getResponse.employer.surname
    document.getElementById('data_patronymic').innerHTML = getResponse.employer.patronymic
    document.getElementById('data_patronymic_2').innerHTML = getResponse.employer.patronymic
    document.getElementById('data_email').innerHTML = getResponse.employer.email
    document.getElementById('data_phone').innerHTML = getResponse.employer.phone
    document.getElementById('data_phone_2').innerHTML = getResponse.employer.phone
}

document.addEventListener("DOMContentLoaded", function () {
    getMe();
})

async function patch_field(field) {
    const name = document.getElementById(`new_${field}`).value
    const patchResponse = await makeRequest({
        method: 'PATCH',
        url: '/api/employers/me',
        data: {
            key: field,
            value: name
        }
    })
    location.reload(true);
}

window.patch_field = patch_field
