import {apiUrl, makeRequest} from "/frontend/js/utils.js";

async function create_company(){
    const name = document.getElementById('name').value
    const description = document.getElementById('description').value
    const response = await makeRequest({
        method: 'POST',
        url: '/api/companies',
        data:{
            name,
            description
        }
    })
    console.log(response)
    if (response){
         window.location.href = apiUrl + '/companies/' + response.company.id
    }
}
window.create_company = create_company