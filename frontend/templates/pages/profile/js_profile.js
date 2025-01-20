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
}

document.addEventListener("DOMContentLoaded", function () {
    getMe();
})
