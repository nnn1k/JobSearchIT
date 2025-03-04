import {apiUrl, makeRequest} from '/frontend/js/utils.js';
import {hideLoadingIndicator, showLoadingIndicator} from '/frontend/js/functions_for_loading.js'

function createTrashBtn(func, obj) {
    const trashBtn = document.createElement('button');
    const img = document.createElement("img");
    img.src = "/frontend/pictures/trash_can.webp";
    img.style.width = "27px";
    img.style.height = "27px";
    trashBtn.style.border = 'None'
    trashBtn.style.backgroundColor = '#f2f2f2;'
    trashBtn.style.cursor = 'pointer'
    trashBtn.appendChild(img);

    trashBtn.onclick = async () => await func(obj)
    return trashBtn
}

async function deleteVacancy(vacancy) {
    const loadingIndicator = showLoadingIndicator();
    const deleteResponse = await makeRequest({
        method: 'DELETE',
        url: `/api/vacancy/${vacancy.id}`
    })
    hideLoadingIndicator(loadingIndicator)
    window.location.href = apiUrl + `/companies/${vacancy.company_id}`
}

async function deleteResume(resume) {
    const loadingIndicator = showLoadingIndicator();
    const deleteResponse = await makeRequest({
        method: 'DELETE',
        url: `/api/workers/resumes/${resume.id}`
    })
    hideLoadingIndicator(loadingIndicator)
    window.location.href = apiUrl + `/worker/resumes`
}

export function createTrashBtnResumes(resume){
    return createTrashBtn(deleteResume, resume)
}
export function createTrashBtnVacancy(vacancy){
    return createTrashBtn(deleteVacancy, vacancy)
}