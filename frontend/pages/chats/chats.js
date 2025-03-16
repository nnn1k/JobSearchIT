import {populateChatList, openChat} from "/frontend/pages/chats/renderChats/renderChatForWorker.js";
import {hideLoadingIndicator, showLoadingIndicator} from "../../js/functions_for_loading.js";
import {apiUrl, makeRequest} from "../../js/utils.js";

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
    const currentUrl = window.location.href;
    console.log(currentUrl)
    const url = new URL(currentUrl);
    const chatId = url.searchParams.get("chatId");
    populateChatList(getResponse.chats)
    if (chatId){
        const intChatID = Number(chatId)
        openChat(intChatID, getResponse.chats)
        hideLoadingIndicator(loadingIndicator)
        return
    }

    hideLoadingIndicator(loadingIndicator)



}