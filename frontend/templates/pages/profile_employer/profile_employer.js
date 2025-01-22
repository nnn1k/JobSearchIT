import {apiUrl, makeRequest} from "../../../js/utils.js";

function hide_feild(row, row_edit) {
    const feild_array = [['row_by_name', 'row_by_edit_name'], ['row_by_surname', 'row_by_edit_surname'],['row_by_patronymic', 'row_by_edit_patronymic'],
    ['row_by_phone', 'row_by_edit_phone'], ['row_by_сompany', 'row_by_edit_сompany']]
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
        if ($(`#${new_feild_array[i][0]}`).is(':hidden')) {
            $(`#${new_feild_array[i][0]}`).toggle(300);

            $(`#${new_feild_array[i][1]}`).toggle(300);

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
window.hide_field = hide_feild
window.cancel_btn = cancel_btn