export function showNotification(message) {
    const notificationContainer = document.getElementById('notification-container');

    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;


    notificationContainer.appendChild(notification);


    requestAnimationFrame(() => {
        notification.classList.add('show');
    });


    setTimeout(() => {
        notification.classList.remove('show');

        setTimeout(() => {
            notificationContainer.removeChild(notification);
        }, 500);
    }, 3000);
}