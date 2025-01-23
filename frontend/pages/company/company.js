import {apiUrl, makeRequest} from "/frontend/js/utils.js";

document.addEventListener('DOMContentLoaded', function () {
    getCompany()
})

async function getCompany() {
    const company_id = location.pathname.split('/')[2]
    const getResponse = await makeRequest({
        method: 'GET',
        url: `/api/companies/${company_id}`
    })
    console.log(getResponse)
    const company = getResponse.company;
    document.getElementById('company_name').innerHTML = company.name;
    document.getElementById('company_description').innerHTML = company.description;
    if (getResponse.can_update) {
        document.getElementById('can_update').style.display = 'block';
    }
}

async function update_company(){
    const company_id = location.pathname.split('/')[2]
    const description = document.getElementById('')
    const putResponse = await makeRequest({
        method: 'PUT',
        url: `/api/companies/${company_id}`,
        data: {
            description
        }
    })
    location.reload(true)
}

window.update_company = update_company
$(document).ready(function () {
    const button_desc = document.getElementById('switch_description')
    const button_vac = document.getElementById('switch_vacancy')
    $("#switch_description").click(function () {
        $(".company_description").toggle();
        $(".company_vacancy").toggle();
        swap(button_desc, button_vac)
    });
    $("#switch_vacancy").click(function () {
        $(".company_description").toggle();
        $(".company_vacancy").toggle();
        swap(button_vac, button_desc)
    });
});

function swap(button1, button2) {
    button1.disabled = true;
    button2.disabled = false;
}