export const apiUrl = 'http://127.0.0.1:8000'

export async function makeRequest(request) {
    const response = await fetch(
        apiUrl + request.url,
        {
            method: request.method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(request.data)
        })
    if (response.ok) {
        const data = await response.json()
        return data
    } else if (response.status === 401) {
        console.error('Ошибка 401: Необходима авторизация.');
        alert('Необходима авторизация. Пожалуйста, войдите в систему.');
    } else if (response.status === 404) {
        console.error('Ошибка 404: Ресурс не найден.');
        alert('Запрашиваемая страница не найдена.');
    } else if (response.status === 500) {
        console.error('Ошибка 500: Внутренняя ошибка сервера.');
        alert('Произошла ошибка на сервере. Попробуйте позже.');
    }
}


