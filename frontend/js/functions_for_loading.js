export function showLoadingIndicator() {
    const loadingIndicator = document.createElement('div');
    loadingIndicator.style.position = 'fixed';
    loadingIndicator.style.top = '50%';
    loadingIndicator.style.left = '50%';
    loadingIndicator.style.transform = 'translate(-50%, -50%)';
    loadingIndicator.style.zIndex = '1000';
    loadingIndicator.style.backgroundColor = '#f8f8f8';
    loadingIndicator.style.color = '#333';
    loadingIndicator.style.padding = '20px';
    loadingIndicator.style.borderRadius = '10px';
    loadingIndicator.style.textAlign = 'center';
    loadingIndicator.style.boxShadow = '0 0 20px rgba(0, 0, 0, 0.5)';


    const backgroundOverlay = document.createElement('div');
    backgroundOverlay.style.position = 'fixed';
    backgroundOverlay.style.top = '0';
    backgroundOverlay.style.left = '0';
    backgroundOverlay.style.width = '100%';
    backgroundOverlay.style.height = '100%';
    backgroundOverlay.style.backgroundColor = 'rgba(0, 0, 0, 0.001)';
    backgroundOverlay.style.zIndex = '999';
    backgroundOverlay.style.pointerEvents = 'auto';


    loadingIndicator.style.animation = 'fadeIn 0.5s';
    loadingIndicator.innerHTML = `
        <img src="/frontend/pictures/loading.gif" alt="Загрузка..." style="width: 80px;">
        <p>Загрузка...</p>
        <style>
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
        </style>`;
    backgroundOverlay.appendChild(loadingIndicator)
    document.body.appendChild(backgroundOverlay);
    return backgroundOverlay;
}

export function hideLoadingIndicator(loadingIndicator) {
    document.body.removeChild(loadingIndicator);
}

window.showLoadingIndicator = showLoadingIndicator
window.hideLoadingIndicator = hideLoadingIndicator