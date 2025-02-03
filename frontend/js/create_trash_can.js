import {apiUrl, makeRequest} from '/frontend/js/utils.js';


export function showTrashBtn(vacancy_id) {
    const trashBtn = document.createElement('button');
    const img = document.createElement("img");
    img.src = "/frontend/pictures/trash_can.webp";
    img.style.width = "27px";
    img.style.height = "27px";
    trashBtn.style.border = 'None'
    trashBtn.style.backgroundColor = 'white'
    trashBtn.appendChild(img);

    trashBtn.onclick = async function () {
        const deleteResponse = await makeRequest({
            method: 'DELETE',
            url: `/api/vacancy/${vacancy_id}`
        })
        alert("хуй соси дура ебанная пидр чмо залупа дота кал эщкере эщкерембус тварь скуф")
        console.log(deleteResponse)
        location.reload(true);
    };
    return trashBtn
}

