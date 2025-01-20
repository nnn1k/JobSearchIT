import {apiUrl, makeRequest} from "../../../js/utils.js";

document.getElementById('link_for_edit_name').addEventListener('click', function (event) {
    event.preventDefault();
    $(document).ready(function () {
        if ($('#row_by_surname').is(':hidden')) {
            $("#row_by_surname").toggle(1000);
            $("#row_by_edit_surname").toggle(1000);
        }
        if ($('#row_by_patronymic').is(':hidden')) {
            $("#row_by_patronymic").toggle(1000);
            $("#row_by_edit_patronymic").toggle(1000);
        }
        if ($('#row_by_phone').is(':hidden')) {
            $("#row_by_phone").toggle(1000);
            $("#row_by_edit_phone").toggle(1000);
        }
        if ($('#row_by_birthday').is(':hidden')) {
            $("#row_by_birthday").toggle(1000);
            $("#row_by_edit_birthday").toggle(1000);
        }
        if ($('#row_by_gender').is(':hidden')) {
            $("#row_by_gender").toggle(1000);
            $("#row_by_edit_gender").toggle(1000);
        }
        if ($('#row_by_city').is(':hidden')) {
            $("#row_by_city").toggle(1000);
            $("#row_by_edit_city").toggle(1000);
        }
        $("#row_by_name").toggle(1000);
        $("#row_by_edit_name").toggle(1000);
    });
});


$(document).ready(function () {
    $("#cancel_btn").click(function () {
        $("#row_by_name").toggle(1000);
        $("#row_by_edit_name").toggle(1000);
    });
});

document.getElementById('link_for_edit_surname').addEventListener('click', function (event) {
    event.preventDefault();
    $(document).ready(function () {
        if ($('#row_by_name').is(':hidden')) {
            $("#row_by_name").toggle(1000);
            $("#row_by_edit_name").toggle(1000);
        }
        if ($('#row_by_patronymic').is(':hidden')) {
            $("#row_by_patronymic").toggle(1000);
            $("#row_by_edit_patronymic").toggle(1000);
        }
        if ($('#row_by_phone').is(':hidden')) {
            $("#row_by_phone").toggle(1000);
            $("#row_by_edit_phone").toggle(1000);
        }
        if ($('#row_by_birthday').is(':hidden')) {
            $("#row_by_birthday").toggle(1000);
            $("#row_by_edit_birthday").toggle(1000);
        }
        if ($('#row_by_gender').is(':hidden')) {
            $("#row_by_gender").toggle(1000);
            $("#row_by_edit_gender").toggle(1000);
        }
        if ($('#row_by_city').is(':hidden')) {
            $("#row_by_city").toggle(1000);
            $("#row_by_edit_city").toggle(1000);
        }
        $("#row_by_surname").toggle(1000);
        $("#row_by_edit_surname").toggle(1000);
    });
});

$(document).ready(function () {
    $("#cancel_btn_for_surname").click(function () {
        $("#row_by_surname").toggle(1000);
        $("#row_by_edit_surname").toggle(1000);
    });
});

document.getElementById('link_for_edit_patronymic').addEventListener('click', function (event) {
    event.preventDefault();
    $(document).ready(function () {
        if ($('#row_by_name').is(':hidden')) {
            $("#row_by_name").toggle(1000);
            $("#row_by_edit_name").toggle(1000);
        }
        if ($('#row_by_surname').is(':hidden')) {
            $("#row_by_surname").toggle(1000);
            $("#row_by_edit_surname").toggle(1000);
        }
        if ($('#row_by_phone').is(':hidden')) {
            $("#row_by_phone").toggle(1000);
            $("#row_by_edit_phone").toggle(1000);
        }
        if ($('#row_by_birthday').is(':hidden')) {
            $("#row_by_birthday").toggle(1000);
            $("#row_by_edit_birthday").toggle(1000);
        }
        if ($('#row_by_gender').is(':hidden')) {
            $("#row_by_gender").toggle(1000);
            $("#row_by_edit_gender").toggle(1000);
        }
        if ($('#row_by_city').is(':hidden')) {
            $("#row_by_city").toggle(1000);
            $("#row_by_edit_city").toggle(1000);
        }
        $("#row_by_patronymic").toggle(1000);
        $("#row_by_edit_patronymic").toggle(1000);
    });
});

$(document).ready(function () {
    $("#cancel_btn_for_patronymic").click(function () {
        $("#row_by_patronymic").toggle(1000);
        $("#row_by_edit_patronymic").toggle(1000);
    });
});

document.getElementById('link_for_edit_phone').addEventListener('click', function (event) {
    event.preventDefault();
    $(document).ready(function () {
        if ($('#row_by_name').is(':hidden')) {
            $("#row_by_name").toggle(1000);
            $("#row_by_edit_name").toggle(1000);
        }
        if ($('#row_by_surname').is(':hidden')) {
            $("#row_by_surname").toggle(1000);
            $("#row_by_edit_surname").toggle(1000);
        }
        if ($('#row_by_patronymic').is(':hidden')) {
            $("#row_by_patronymic").toggle(1000);
            $("#row_by_edit_patronymic").toggle(1000);
        }
        if ($('#row_by_birthday').is(':hidden')) {
            $("#row_by_birthday").toggle(1000);
            $("#row_by_edit_birthday").toggle(1000);
        }
        if ($('#row_by_gender').is(':hidden')) {
            $("#row_by_gender").toggle(1000);
            $("#row_by_edit_gender").toggle(1000);
        }
        if ($('#row_by_city').is(':hidden')) {
            $("#row_by_city").toggle(1000);
            $("#row_by_edit_city").toggle(1000);
        }
        $("#row_by_phone").toggle(1000);
        $("#row_by_edit_phone").toggle(1000);
    });
});

$(document).ready(function () {
    $("#cancel_btn_for_phone").click(function () {
        $("#row_by_phone").toggle(1000);
        $("#row_by_edit_phone").toggle(1000);
    });
});

document.getElementById('link_for_edit_birthday').addEventListener('click', function (event) {
    event.preventDefault();
    $(document).ready(function () {
        if ($('#row_by_name').is(':hidden')) {
            $("#row_by_name").toggle(1000);
            $("#row_by_edit_name").toggle(1000);
        }
        if ($('#row_by_surname').is(':hidden')) {
            $("#row_by_surname").toggle(1000);
            $("#row_by_edit_surname").toggle(1000);
        }
        if ($('#row_by_patronymic').is(':hidden')) {
            $("#row_by_patronymic").toggle(1000);
            $("#row_by_edit_patronymic").toggle(1000);
        }
        if ($('#row_by_phone').is(':hidden')) {
            $("#row_by_phone").toggle(1000);
            $("#row_by_edit_phone").toggle(1000);
        }
        if ($('#row_by_gender').is(':hidden')) {
            $("#row_by_gender").toggle(1000);
            $("#row_by_edit_gender").toggle(1000);
        }
        if ($('#row_by_city').is(':hidden')) {
            $("#row_by_city").toggle(1000);
            $("#row_by_edit_city").toggle(1000);
        }
        $("#row_by_birthday").toggle(1000);
        $("#row_by_edit_birthday").toggle(1000);
    });
});

$(document).ready(function () {
    $("#cancel_btn_for_birthday").click(function () {
        $("#row_by_birthday").toggle(1000);
        $("#row_by_edit_birthday").toggle(1000);
    });
});

document.getElementById('link_for_edit_city').addEventListener('click', function (event) {
    event.preventDefault();
    $(document).ready(function () {
        if ($('#row_by_name').is(':hidden')) {
            $("#row_by_name").toggle(1000);
            $("#row_by_edit_name").toggle(1000);
        }
        if ($('#row_by_surname').is(':hidden')) {
            $("#row_by_surname").toggle(1000);
            $("#row_by_edit_surname").toggle(1000);
        }
        if ($('#row_by_patronymic').is(':hidden')) {
            $("#row_by_patronymic").toggle(1000);
            $("#row_by_edit_patronymic").toggle(1000);
        }
        if ($('#row_by_phone').is(':hidden')) {
            $("#row_by_phone").toggle(1000);
            $("#row_by_edit_phone").toggle(1000);
        }
        if ($('#row_by_birthday').is(':hidden')) {
            $("#row_by_birthday").toggle(1000);
            $("#row_by_edit_birthday").toggle(1000);
        }
        if ($('#row_by_gender').is(':hidden')) {
            $("#row_by_gender").toggle(1000);
            $("#row_by_edit_gender").toggle(1000);
        }
        $("#row_by_city").toggle(1000);
        $("#row_by_edit_city").toggle(1000);
    });
});


$(document).ready(function () {
    $("#cancel_btn_for_city").click(function () {
        $("#row_by_city").toggle(1000);
        $("#row_by_edit_city").toggle(1000);
    });
});

async function getMe(){
    const getResponse = await makeRequest({
            method: 'GET',
            url: '/api/workers/me',
            }
        )
    console.log(getResponse)
    document.getElementById('data_name').innerHTML=getResponse.worker.name
    document.getElementById('data_name_2').innerHTML=getResponse.worker.name
    document.getElementById('data_surname').innerHTML=getResponse.worker.surname
    document.getElementById('data_surname_2').innerHTML=getResponse.worker.surname
    document.getElementById('data_patronymic').innerHTML=getResponse.worker.patronymic
    document.getElementById('data_patronymic_2').innerHTML=getResponse.worker.patronymic
    document.getElementById('data_email').innerHTML=getResponse.worker.email
    document.getElementById('data_phone').innerHTML=getResponse.worker.phone
    document.getElementById('data_phone_2').innerHTML=getResponse.worker.phone
    document.getElementById('data_birthday').innerHTML=getResponse.worker.birthday
    document.getElementById('data_birthday_2').innerHTML=getResponse.worker.birthday
    document.getElementById('data_city').innerHTML=getResponse.worker.city
    document.getElementById('data_city_2').innerHTML=getResponse.worker.city
}

document.addEventListener("DOMContentLoaded", function () {
    getMe();
})

async function patch_field(field) {
    const name = document.getElementById(`new_${field}`).value
    const patchResponse = await makeRequest({
        method: 'PATCH',
        url: '/api/workers/me',
        data: {
            key: field,
            value: name
        }
    })
    location.reload(true);
}

window.patch_field = patch_field
