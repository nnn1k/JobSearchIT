import {formatDateTime} from "/frontend/js/timefunc.js";
import {showLoadingIndicator, hideLoadingIndicator} from "/frontend/js/functions_for_loading.js";
import {apiUrl} from "../../../js/utils.js";

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

export function populateChatList(chats) {
    const chatListElement = document.getElementById('chatList');

    chats.forEach(chat => {
        const chatItem = document.createElement('div');
        chatItem.className = 'chat-item';
        chatItem.dataset.chatId = chat.id;
        const userType = getCookie('user_type')
        var lastMessage
        if (chat.last_message === null){
            lastMessage = ''
        }
        else {
            lastMessage = chat.last_message.message
        }
        if (userType === 'worker') {
            chatItem.innerHTML = `
                    <div class="job-title">${chat.response.vacancy.profession.title}</div>
                    <div class="company-name">${chat.response.vacancy.company.name}</div>
                    <div class="last-message">${lastMessage}</div>
                `;

            chatItem.addEventListener('click', () => openChat(chat.id, chats));
            chatListElement.appendChild(chatItem);
        }
        if (userType === 'employer') {
            chatItem.innerHTML = `
                    <div class="job-title">${chat.response.resume.worker.name} ${chat.response.resume.worker.surname}</div>
                    <div class="company-name">${chat.response.resume.profession.title}</div>
                    <div class="last-message">${lastMessage}</div>
                `;

            chatItem.addEventListener('click', () => openChat(chat.id, chats));
            chatListElement.appendChild(chatItem);
        }
    })
}

export function openChat(chatId, chats) {
    const loadingIndicator = showLoadingIndicator();
    const chatWindow = document.getElementById('chatWindow');
    const url = new URL(window.location);
    url.searchParams.set('chatId', chatId); // Устанавливаем новый параметр

    // Обновляем адресную строку без перезагрузки страницы
    window.history.pushState({}, '', url);
    const ws = new WebSocket(`ws://127.0.0.1:8000/api/chats/ws/${chatId}`);
    ws.onopen = function () {
        ws.send(JSON.stringify({'message': '', 'type': 'join', 'chat_id': chatId}))
    }
    ws.onmessage = function (event) {

        const message = JSON.parse(event.data)
        const jsonMessages = JSON.parse(message)
        const messageElement = document.createElement('div');
        if (jsonMessages.type === 'message') {

            const userType = getCookie('user_type')

            if (jsonMessages.sender_type === userType) {
                messageElement.className = `message sent`;
            } else {
                messageElement.className = `message received`;
            }
            messageElement.innerHTML = `
                    <div class="message-text">${jsonMessages.message}</div>   
                    <div class="message-time">${formatDateTime(jsonMessages.created_at).replace("2025 года", "")}</div>  
               `;
            chatMessages.appendChild(messageElement);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        if (jsonMessages.type === 'join') {
            hideLoadingIndicator(loadingIndicator)
            const userType = getCookie('user_type')

            if (userType === 'worker'){
                chatWindow.innerHTML = `
                <div class="chat-header">
                    <div class="job-title">${selectedChat.response.vacancy.profession.title}</div>
                    <div class="company-name">${selectedChat.response.vacancy.company.name}</div>
                </div>
                <div class="chat-messages" id="chatMessages"></div>
                <div class="message-input-container">
                    <input type="text" class="message-input" id="messageInput" placeholder="Введите сообщение...">
                    <button class="send-button" id="sendButton">➤</button>
                </div>
            `;
            }
            if (userType === 'employer'){
                chatWindow.innerHTML = `
                <div class="chat-header">
                    <div class="job-title">${selectedChat.response.resume.worker.name} ${selectedChat.response.resume.worker.surname}</div>
                    <div class="company-name">${selectedChat.response.resume.profession.title}</div>
                </div>
                <div class="chat-messages" id="chatMessages"></div>
                <div class="message-input-container">
                    <input type="text" class="message-input" id="messageInput" placeholder="Введите сообщение...">
                    <button class="send-button" id="sendButton">➤</button>
                </div>
            `;
            }



            const chatMessages = document.getElementById('chatMessages');
            sendButton.addEventListener('click', sendMessage);
            messageInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
            jsonMessages.messages.forEach(message => {
                const jsonMessage = JSON.parse(message)
                const messageElement = document.createElement('div');
                const userType = getCookie('user_type')

                if (jsonMessage.sender_type === userType) {
                    messageElement.className = `message sent`;
                } else {
                    messageElement.className = `message received`;
                }
                messageElement.innerHTML = `
                    <div class="message-text">${jsonMessage.message}</div>   
                    <div class="message-time">${formatDateTime(jsonMessage.created_at).replace("2025 года", "")}</div>  
               `;
                chatMessages.appendChild(messageElement);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            });
        }
    }

    document.querySelectorAll('.chat-item').forEach(item => {
        item.classList.remove('active');
    });

    //
    document.querySelector(`.chat-item[data-chat-id="${chatId}"]`).classList.add('active');

    // Находим выбранный чат
    const selectedChat = chats.find(chat => chat.id === chatId);


    function sendMessage() {
        // Добавляем функциональность отправки сообщений
        const messageInput = document.getElementById('messageInput');
        const sendButton = document.getElementById('sendButton');

        console.log(chatId)
        const messageText = messageInput.value.trim();
        if (messageText) {
            const data = {
                "message": messageText,
                'type': 'message',
                'chat_id': chatId,
            }
            ws.send(JSON.stringify(data))
            // Создаем новое сообщение
            const newMessage = {
                text: messageText,
                time: getCurrentTime(),
                type: 'sent'
            };



            // Обновляем последнее сообщение в списке чатов
            const chatItem = document.querySelector(`.chat-item[data-chat-id="${chatId}"]`);
            chatItem.querySelector('.last-message').textContent = messageText;


            // Очищаем поле ввода
            messageInput.value = '';

            // Прокручиваем к новому сообщению
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
}




// Функция для получения текущего времени
function getCurrentTime() {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
}

// Инициализация интерфейса чата


window.populateChatList = populateChatList