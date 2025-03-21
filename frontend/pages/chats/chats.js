import {populateChatList, openChat} from "/frontend/pages/chats/renderChats/renderChat.js";
import {hideLoadingIndicator, showLoadingIndicator} from "/frontend/js/functions_for_loading.js";
import {apiUrl, makeRequest, getCookie} from "/frontend/js/utils.js";

document.addEventListener('DOMContentLoaded', function () {
    getChats()
})


async function getChats() {
    const loadingIndicator = showLoadingIndicator();
    const getResponse = await makeRequest({
        method: 'GET',
        url: `/api/chats`
    })
    console.log(getResponse)
    const currentUrl = window.location.href;
    const url = new URL(currentUrl);
    const chatId = url.searchParams.get("chatId");
    populateChatList(getResponse.chats)
    if (chatId){
        const intChatID = Number(chatId)
        openChat(intChatID, getResponse.chats)
    }

    hideLoadingIndicator(loadingIndicator)



}