import {apiUrl, makeRequest} from "../../../js/utils.js";

function hide_feild(row, row_edit) {
    const feild_array = [['row_by_name', 'row_by_edit_name'], ['row_by_surname', 'row_by_edit_surname'],['row_by_patronymic', 'row_by_edit_patronymic'],
    ['row_by_phone', 'row_by_edit_phone'], ['row_by_birthday', 'row_by_edit_birthday'],['row_by_gender', 'row_by_edit_gender'],['row_by_city', 'row_by_edit_city']]
    for (let i = 0; i < feild_array.length; i++) {
        const index = feild_array[i].indexOf(row);
        if (index !== -1) {
            feild_array[i].splice(index, 1);
        }
    }
    for (let i = 0; i < feild_array.length; i++) {
        const index = feild_array[i].indexOf(row_edit);
        if (index !== -1) {
            feild_array[i].splice(index, 1);
        }
    }
    const new_feild_array = feild_array.filter(row => row.length > 0);
    for (let i = 0; i < new_feild_array.length; i++){
        console.log(new_feild_array[i][0])
        if ($(`#${new_feild_array[i][0]}`).is(':hidden')) {
            $(`#${new_feild_array[i][0]}`).toggle(300);
            console.log(i[0])
            $(`#${new_feild_array[i][1]}`).toggle(300);
            console.log(i[1])
        }
    }
    $(`#${row}`).toggle(300);
    $(`#${row_edit}`).toggle(300);
}

function cancel_btn(row, row_edit, btn){
    $(`#${btn}`).click(function () {
        $(`#${row}`).toggle(300);
        $(`#${row_edit}`).toggle(300);
    });
}

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

document.getElementById('link_for_edit_birthday').addEventListener('click', function (event) {
    event.preventDefault();
    $(document).ready(function () {
        hide_feild('row_by_birthday', 'row_by_edit_birthday')
    });
});

$(document).ready(function () {
    cancel_btn('row_by_birthday', 'row_by_edit_birthday', 'cancel_btn_for_birthday')
});

document.getElementById('link_for_edit_city').addEventListener('click', function (event) {
    event.preventDefault();
    $(document).ready(function () {
        hide_feild('row_by_city', 'row_by_edit_city')
    });
});


$(document).ready(function () {
    cancel_btn('row_by_city', 'row_by_edit_city', 'cancel_btn_for_city')
});

async function getMe() {
    const getResponse = await makeRequest({
            method: 'GET',
            url: '/api/workers/me',
        }
    )
    console.log(getResponse)
    document.getElementById('data_name').innerHTML = getResponse.worker.name
    document.getElementById('data_name_2').innerHTML = getResponse.worker.name
    document.getElementById('data_surname').innerHTML = getResponse.worker.surname
    document.getElementById('data_surname_2').innerHTML = getResponse.worker.surname
    document.getElementById('data_patronymic').innerHTML = getResponse.worker.patronymic
    document.getElementById('data_patronymic_2').innerHTML = getResponse.worker.patronymic
    document.getElementById('data_email').innerHTML = getResponse.worker.email
    document.getElementById('data_phone').innerHTML = getResponse.worker.phone
    document.getElementById('data_phone_2').innerHTML = getResponse.worker.phone
    document.getElementById('data_birthday').innerHTML = getResponse.worker.birthday
    document.getElementById('data_birthday_2').innerHTML = getResponse.worker.birthday
    document.getElementById('data_city').innerHTML = getResponse.worker.city
    document.getElementById('data_city_2').innerHTML = getResponse.worker.city
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
window.hide_field = hide_feild
window.cancel_btn = cancel_btn