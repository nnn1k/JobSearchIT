export function showNotification(message) {
    const notificationContainer = document.getElementById('notification-container');

    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;

    // Добавляем уведомление в контейнер
    notificationContainer.appendChild(notification);

    // Появление уведомления
    requestAnimationFrame(() => {
        notification.classList.add('show');
    });

    // Удаляем уведомление через 3 секунды
    setTimeout(() => {
        notification.classList.remove('show');
        // Удаляем элемент после завершения анимации
        setTimeout(() => {
            notificationContainer.removeChild(notification);
        }, 500); // Время анимации
    }, 3000); // Время отображения
}