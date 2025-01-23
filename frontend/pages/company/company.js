import {apiUrl, makeRequest} from "/frontend/js/utils.js";

document.addEventListener('DOMContentLoaded', function (){
    getCompany()
})

async function getCompany(){
    const company_id = location.pathname.split('/')[2]
    const getResponse = await makeRequest({
        method: 'GET',
        url: `/api/companies/${company_id}`
    })
    console.log(getResponse)
    const company = getResponse.company;
    document.getElementById('company_name').innerHTML = company.name;
    document.getElementById('company_description').innerHTML = company.description;
    if (getResponse.can_update){
        document.getElementById('can_update').style.display = 'block';
    }
}