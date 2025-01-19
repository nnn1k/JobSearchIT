document.getElementById('link_for_edit_name').addEventListener('click', function (event) {
    event.preventDefault();
    $(document).ready(function () {
            $("#row_by_name").toggle();
            $("#row_by_edit_name").toggle();
    });
});


$(document).ready(function() {
    $("#cancel_btn").click(function() {
        $("#row_by_name").toggle();
        $("#row_by_edit_name").toggle();
    });
});

document.getElementById('link_for_edit_surname').addEventListener('click', function (event) {
    event.preventDefault();
    $(document).ready(function () {
            $("#row_by_surname").toggle();
            $("#row_by_edit_surname").toggle();
    });
});

$(document).ready(function() {
    $("#cancel_btn_for_surname").click(function() {
        $("#row_by_surname").toggle();
        $("#row_by_edit_surname").toggle();
    });
});

document.getElementById('link_for_edit_patronymic').addEventListener('click', function (event) {
    event.preventDefault();
    $(document).ready(function () {
            $("#row_by_patronymic").toggle();
            $("#row_by_edit_patronymic").toggle();
    });
});

$(document).ready(function() {
    $("#cancel_btn_for_patronymic").click(function() {
        $("#row_by_patronymic").toggle();
        $("#row_by_edit_patronymic").toggle();
    });
});

document.getElementById('link_for_edit_phone').addEventListener('click', function (event) {
    event.preventDefault();
    $(document).ready(function () {
            $("#row_by_phone").toggle();
            $("#row_by_edit_phone").toggle();
    });
});

$(document).ready(function() {
    $("#cancel_btn_for_phone").click(function() {
        $("#row_by_phone").toggle();
        $("#row_by_edit_phone").toggle();
    });
});

document.getElementById('link_for_edit_birthday').addEventListener('click', function (event) {
    event.preventDefault();
    $(document).ready(function () {
            $("#row_by_birthday").toggle();
            $("#row_by_edit_birthday").toggle();
    });
});

$(document).ready(function() {
    $("#cancel_btn_for_birthday").click(function() {
        $("#row_by_birthday").toggle();
        $("#row_by_edit_birthday").toggle();
    });
});

document.getElementById('link_for_edit_gender').addEventListener('click', function (event) {
    event.preventDefault();
    $(document).ready(function () {
            $("#row_by_gender").toggle();
            $("#row_by_edit_gender").toggle();
    });
});

$(document).ready(function() {
    $("#cancel_btn_for_gender").click(function() {
        $("#row_by_gender").toggle();
        $("#row_by_edit_gender").toggle();
    });
});

document.getElementById('link_for_edit_city').addEventListener('click', function (event) {
    event.preventDefault();
    $(document).ready(function () {
            $("#row_by_city").toggle();
            $("#row_by_edit_city").toggle();
    });
});


$(document).ready(function() {
    $("#cancel_btn_for_city").click(function() {
        $("#row_by_city").toggle();
        $("#row_by_edit_city").toggle();
    });
});
