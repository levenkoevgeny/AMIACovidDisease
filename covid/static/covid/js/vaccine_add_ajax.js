$("form").submit(function (e) {

    e.preventDefault();

    let form_data = $("form").serializeArray();
    let button_value = $('#id-vaccine-add-button').val();

    let url = ''

    if (button_value === 'Save') {
        let employee_id = $('#id-employee-id').val();
        url = `/covid/${employee_id}/vaccines-add`
    }
    if (button_value === 'Update') {
        let vac_course_id = $('#id-vaccine-course-id').val();
        url = `/covid/${vac_course_id}/vaccines-update`
    }

    $.ajax({
        url: url,
        method: "POST",
        dataType: 'json',
        data: form_data,
        timeout: 100000,
        success: function (data) {
            console.log(data)
            window.opener.location.href = window.opener.location.href;
            window.close();
        },
        error: function (e) {
            console.log("ERROR: ", e);
        },
        done: function (e) {
            console.log("DONE");
        }
    });
});
