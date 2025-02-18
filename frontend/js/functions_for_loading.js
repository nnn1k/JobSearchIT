export function showLoadingIndicator() {
    const loadingIndicator = document.createElement('div');
    loadingIndicator.style.position = 'fixed';
    loadingIndicator.style.top = '50%';
    loadingIndicator.style.left = '50%';
    loadingIndicator.style.transform = 'translate(-50%, -50%)';
    loadingIndicator.style.zIndex = '1000';
    loadingIndicator.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
    loadingIndicator.style.color = '#333';
    loadingIndicator.style.padding = '20px';
    loadingIndicator.style.borderRadius = '10px';
    loadingIndicator.style.textAlign = 'center';
    loadingIndicator.style.boxShadow = '0 0 20px rgba(0, 0, 0, 0.5)';

    // Добавляем анимацию
    loadingIndicator.style.animation = 'fadeIn 0.5s';
    loadingIndicator.innerHTML = `
        <img src="https://i.gifer.com/VAyR.gif" alt="Загрузка..." style="width: 50px;">
        <p>Загрузка...</p>
        <style>
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
        </style>`;

    document.body.appendChild(loadingIndicator);
    return loadingIndicator;
}

export function hideLoadingIndicator(loadingIndicator) {
    document.body.removeChild(loadingIndicator);
}

window.showLoadingIndicator = showLoadingIndicator
window.hideLoadingIndicator = hideLoadingIndicator