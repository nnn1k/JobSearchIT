import {populateChatList} from "/frontend/pages/chats/renderChats/renderChatForWorker.js";
import {hideLoadingIndicator, showLoadingIndicator} from "../../js/functions_for_loading.js";
import {makeRequest} from "../../js/utils.js";

document.addEventListener('DOMContentLoaded', function () {
    getChats()
})

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}


async function getChats() {
    const loadingIndicator = showLoadingIndicator();
    const getResponse = await makeRequest({
        method: 'GET',
        url: `/api/chats`
    })
    console.log(getResponse)
    const userType = getCookie('user_type')
    if (userType === 'worker') {
        populateChatList(getResponse.chats)
    }
    if (userType === 'employer') {
        populateChatList(getResponse.chats)
    }
    hideLoadingIndicator(loadingIndicator)



}