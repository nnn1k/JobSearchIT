

export const apiUrl = 'https://' + window.location.host;

export async function makeRequest(request) {
    const response = await fetch(
        request.url,
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
    } else if (response.status >= 400 && response.status < 500) {
        const errorData = await response.json()
        console.log(errorData)
        alert('error')
    } else if (response.status === 500) {
        console.error('Ошибка 500: Внутренняя ошибка сервера.');
        alert('Произошла ошибка на сервере. Попробуйте позже.');
    }
}


export function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}