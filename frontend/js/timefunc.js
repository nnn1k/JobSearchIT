export function formatDateTime(isoDateString) {
    const trimmedDateString = isoDateString.slice(0, 26);
    const dateObject = new Date(trimmedDateString);

    const months = [
        "января", "февраля", "марта", "апреля", "мая", "июня",
        "июля", "августа", "сентября", "октября", "ноября", "декабря"
    ];

    const day = dateObject.getDate();
    const month = months[dateObject.getMonth()];
    const year = dateObject.getFullYear();

    const hours = String(dateObject.getHours()).padStart(2, '0');
    const minutes = String(dateObject.getMinutes()).padStart(2, '0');
    const seconds = String(dateObject.getSeconds()).padStart(2, '0');

    return `${day} ${month} ${year} года, ${hours}:${minutes}`;
    // return `${day} ${month} ${year} года, ${hours}:${minutes}:${seconds}`;
}