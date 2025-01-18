 export const apiUrl= 'http://127.0.0.1:8000'

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
    } else if (response.status == 401){
        console.log('ТЫ ПИДР')
    } else {
        console.error('error:', response.status)
    }
}


