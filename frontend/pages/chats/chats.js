import {formatDateTime} from "/frontend/js/timefunc.js";
import {apiUrl, getCookie} from "/frontend/js/utils.js";

document.addEventListener('DOMContentLoaded', function () {
    createChatSystem()
})

let chats;
let ws;

function getUrlChatId() {
    return new URL(window.location.href).searchParams.get("chatId");
}

function createChatSystem() {
    ws = createChatSocket()

    ws.onmessage = function (event) {
        const response = JSON.parse(JSON.parse(event.data))
        if (response.type === 'message') {
            showMessage(response)
        }
        if (response.type === 'join') {
            createChatWindow(response.messages)
        }
        if (response.type === 'open') {
            chats = response.chats.map(chat => JSON.parse(chat))
            console.log(chats)
            populateChatList(chats)
            const chatId = getUrlChatId()
            if (chatId) {
                openChat(chatId)
            }
        }
    }
}

export function populateChatList(chats) {
    const chatListElement = document.getElementById('chatList');

    chats.forEach(chat => {
        const chatItem = document.createElement('div');
        chatItem.className = 'chat-item';
        chatItem.dataset.chatId = chat.id;
        const userType = getCookie('user_type')
        let lastMessage = ''
        if (chat.last_message !== null) {
            lastMessage = chat.last_message.message
        }
        let titleData
        let underTitleData
        if (userType === 'worker') {
            titleData = `${chat.response.vacancy.profession.title}`
            underTitleData = `${chat.response.vacancy.company.name}`
        }
        if (userType === 'employer') {
            titleData = `${chat.response.resume.worker.name} ${chat.response.resume.worker.surname}`
            underTitleData = `${chat.response.resume.profession.title}`
        }
        chatItem.innerHTML = `
                    <div class="job-title">${titleData}</div>
                    <div class="company-name">${underTitleData}</div>
                    <div class="last-message" id=last-message-for-chat-${chat.id}>${lastMessage}</div>
                `;
        chatItem.addEventListener('click', () => openChat(chat.id, chats));
        chatListElement.appendChild(chatItem);
    })
}

export function openChat(chatId) {
    const url = new URL(window.location);
    url.searchParams.set('chatId', chatId); // Устанавливаем новый параметр
    window.history.pushState({}, '', url);

    document.querySelectorAll('.chat-item').forEach(item => {
        item.classList.remove('active');
    });

    document.querySelector(`.chat-item[data-chat-id="${chatId}"]`).classList.add('active');
    ws.send(JSON.stringify({'type': 'join', 'chat_id': chatId}))
}

function createChatSocket() {

    let new_ws = new WebSocket(`ws://${apiUrl}/api/chats/ws`);

    new_ws.onopen = () => {
        new_ws.send(JSON.stringify({'message': '', 'type': 'open', 'chat_id': ''}))
        console.log('Сокет заработал')
    }

    new_ws.onclose = () => {
        console.log('Сокет упал, пытаемся переподключиться к сокету...');
        setTimeout(createChatSocket, 20000);
    }

    return new_ws
}

function showMessage(message) {
    const chatMessages = document.getElementById('chatMessages');
    const messageElement = document.createElement('div');
    const userType = getCookie('user_type')

    if (message.sender_type === userType) {
        messageElement.className = `message sent`;
    } else {
        messageElement.className = `message received`;
    }
    messageElement.innerHTML = `
                    <div class="message-text">${message.message}</div>   
                    <div class="message-time">${formatDateTime(message.created_at).replace("2025 года", "")}</div>  
               `;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    const lastMessage = document.getElementById(`last-message-for-chat-${message.chat_id}`)
    lastMessage.textContent = message.message
}

function createChatWindow(messages) {
    const chatWindow = document.getElementById('chatWindow');
    const userType = getCookie('user_type')
    const chatId = getUrlChatId()
    const selectedChat = chats.find(chat => chat.id === Number(chatId));
    // шапка (для ролей)
    if (userType === 'worker') {
        chatWindow.innerHTML = `
                <div class="chat-header">
                    <div class="job-title">${selectedChat.response.vacancy.profession.title}</div>
                    <div class="company-name">${selectedChat.response.vacancy.company.name}</div>
                </div>
            `;
    }
    if (userType === 'employer') {
        chatWindow.innerHTML = `
                <div class="chat-header">
                    <div class="job-title">${selectedChat.response.resume.worker.name} ${selectedChat.response.resume.worker.surname}</div>
                    <div class="company-name">${selectedChat.response.resume.profession.title}</div>
                </div>
            `;
    }
    // сообщения
    chatWindow.innerHTML += `<div class="chat-messages" id="chatMessages"></div>
                <div class="message-input-container">
                    <input type="text" class="message-input" id="messageInput" placeholder="Введите сообщение...">
                    <button class="send-button" id="sendButton">➤</button>
                </div>`

    const sendButton = document.getElementById('sendButton');
    const messageInput = document.getElementById('messageInput');

    sendButton.addEventListener('click', () => {
        sendMessage();
    });
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    messages.forEach(message => {
        const jsonMessage = JSON.parse(message)
        showMessage(jsonMessage)
    });
}

function sendMessage() {
    // Добавляем функциональность отправки сообщений
    const messageInput = document.getElementById('messageInput');
    const chatMessages = document.getElementById('chatMessages')
    const chatId = getUrlChatId()

    const messageText = messageInput.value.trim();
    if (messageText) {
        const data = {
            "message": messageText,
            'type': 'message',
            'chat_id': chatId,
        }
        ws.send(JSON.stringify(data))

        // Очищаем поле ввода
        messageInput.value = '';

        // Прокручиваем к новому сообщению
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

// Инициализация интерфейса чата
window.populateChatList = populateChatList