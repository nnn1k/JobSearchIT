export const apiUrl = window.location.protocol + '//' + window.location.host;


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
    } else if (response.status >= 400 && response.status <= 500) {
        const errorData = await response.json()
        console.log(errorData)
        alert(errorData.detail)
    } else if (response.status === 500) {
        console.error('Ошибка 500: Внутренняя ошибка сервера.');
        alert('Произошла ошибка на сервере. Попробуйте позже.');
    }
}


