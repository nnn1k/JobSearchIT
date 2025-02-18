export function print_salary(salaryElement, salary_first, salary_second){
    salaryElement.innerHTML += `<strong>Зарплата:</strong>`;
    if (!salary_first && !salary_second)
            salaryElement.innerHTML += ' Не указана';
        else {
            if (salary_first)
                salaryElement.innerHTML += ` от ${salary_first}`;
            if (salary_second)
                salaryElement.innerHTML += ` до ${salary_second}`;
            salaryElement.innerHTML += ' руб.'
        }
}