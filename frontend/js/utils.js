// Гарантированно используем HTTPS
export const apiUrl = 'https://' + window.location.host;

export async function makeRequest(request) {
    // Обеспечиваем корректный URL запроса
    let requestUrl = request.url;

    // Если URL относительный (начинается с /), добавляем базовый apiUrl
    if (requestUrl.startsWith('/')) {
        requestUrl = apiUrl + requestUrl;
    }
    // Если URL не начинается с http, добавляем https
    else if (!requestUrl.startsWith('http')) {
        requestUrl = apiUrl + '/' + requestUrl;
    }
    // Если URL начинается с http:, принудительно меняем на https:
    else if (requestUrl.startsWith('http:')) {
        requestUrl = requestUrl.replace('http:', 'https:');
    }

    try {
        const response = await fetch(requestUrl, {
            method: request.method,
            headers: {
                'Content-Type': 'application/json',
                // Добавляем CSRF-токен, если используется
                'X-CSRFToken': getCookie('csrftoken') || '',
            },
            credentials: 'include', // Для передачи кук
            body: request.data ? JSON.stringify(request.data) : null,
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            console.error('Request failed:', {
                status: response.status,
                statusText: response.statusText,
                errorData,
            });

            throw new Error(errorData.message || `HTTP error ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Request error:', error);
        alert(error.message || 'Произошла ошибка при выполнении запроса');
        throw error;
    }
}

export function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}