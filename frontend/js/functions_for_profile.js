export function hide_field(row, row_edit) {
    const field_array = [['row_by_name', 'row_by_edit_name'], ['row_by_surname', 'row_by_edit_surname'], ['row_by_patronymic', 'row_by_edit_patronymic'],
        ['row_by_phone', 'row_by_edit_phone'], ['row_by_сompany', 'row_by_edit_сompany'],
        ['row_by_birthday', 'row_by_edit_birthday'],['row_by_gender', 'row_by_edit_gender'],['row_by_city', 'row_by_edit_city']]
    for (let i = 0; i < field_array.length; i++) {
        const index = field_array[i].indexOf(row);
        if (index !== -1) {
            field_array[i].splice(index, 1);
        }
    }
    for (let i = 0; i < field_array.length; i++) {
        const index = field_array[i].indexOf(row_edit);
        if (index !== -1) {
            field_array[i].splice(index, 1);
        }
    }
    const new_field_array = field_array.filter(row => row.length > 0);
    for (let i = 0; i < new_field_array.length; i++) {
        if ($(`#${new_field_array[i][0]}`).is(':hidden')) {
            $(`#${new_field_array[i][0]}`).toggle(300);

            $(`#${new_field_array[i][1]}`).toggle(300);

        }
    }
    $(`#${row}`).toggle(300);
    $(`#${row_edit}`).toggle(300);
}

export function cancel_btn(row, row_edit, btn){
    $(`#${btn}`).click(function () {
        $(`#${row}`).toggle(300);
        $(`#${row_edit}`).toggle(300);
    });
}

window.hide_field = hide_field
window.cancel_btn = cancel_btn