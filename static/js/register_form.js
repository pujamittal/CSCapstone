$(document).ready(function() {
    $("input[name$='usertype']").click(function() {
        var radio_value = $(this).val();

        if (radio_value == 'Student') {
            $("#id_almamater").hide();
            $("label[for='id_almamater']").hide();
            $("#id_about").hide();
            $("label[for='id_about']").hide();
            $("#id_university").show();
            $("label[for='id_university']").show();
            $("#id_company").hide();
            $("label[for='id_company']").hide();
        }
        else if (radio_value == 'Teacher') {
            $("#id_almamater").hide();
            $("label[for='id_almamater']").hide();
            $("#id_about").hide();
            $("label[for='id_about']").hide();
            $("#id_university").show();
            $("label[for='id_university']").show();
            $("#id_company").hide();
            $("label[for='id_company']").hide();
        }
        else if (radio_value == 'Engineer') {
            $("#id_almamater").show();
            $("label[for='id_almamater']").show();
            $("#id_about").show();
            $("label[for='id_about']").show();
            $("#id_university").hide();
            $("label[for='id_university']").hide();
            $("#id_company").show();
            $("label[for='id_company']").show();
        }
    });

    $("#id_almamater").hide();
    $("label[for='id_almamater']").hide();
    $("#id_about").hide();
    $("label[for='id_about']").hide();
    $("#id_university").hide();
    $("label[for='id_university']").hide();
    $("#id_company").hide();
    $("label[for='id_company']").hide();
});