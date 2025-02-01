import {get_user_type} from "/frontend/js/check_user_type.js";

document.addEventListener("DOMContentLoaded", function () {
    const type = get_user_type()
    console.log(type)
})