import {apiUrl, makeRequest} from '/frontend/js/utils.js';


function createTrashBtn(func, obj) {
    const trashBtn = document.createElement('button');
    const img = document.createElement("img");
    img.src = "/frontend/pictures/trash_can.webp";
    img.style.width = "27px";
    img.style.height = "27px";
    trashBtn.style.border = 'None'
    trashBtn.style.backgroundColor = '#f2f2f2;'
    trashBtn.appendChild(img);

    trashBtn.onclick = async () => await func(obj)
    return trashBtn
}

async function deleteVacancy(vacancy) {
    const deleteResponse = await makeRequest({
        method: 'DELETE',
        url: `/api/vacancy/${vacancy.id}`
    })
    console.log(deleteResponse)
    window.location.href = apiUrl + `/companies/${vacancy.company_id}`
}

async function deleteResume(resume) {
    const deleteResponse = await makeRequest({
        method: 'DELETE',
        url: `/api/workers/resumes/${resume.id}`
    })
    console.log(deleteResponse)
    window.location.href = apiUrl + `/worker/resumes`
}

export function createTrashBtnResumes(resume){
    return createTrashBtn(deleteResume, resume)
}
export function createTrashBtnVacancy(vacancy){
    return createTrashBtn(deleteVacancy, vacancy)
}