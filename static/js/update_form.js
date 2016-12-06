$(document).ready(function() {
    if ($("#is_student").length > 0) {
        $("#id_almamater").remove();
        $("label[for='id_almamater']").remove();
        $("#id_about").remove();
        $("label[for='id_about']").remove();
        $("#id_company").remove();
        $("label[for='id_company']").remove();
    }
    else if ($("#is_teacher").length > 0) {
        $("#id_almamater").remove();
        $("label[for='id_almamater']").remove();
        $("#id_about").remove();
        $("label[for='id_about']").remove();
        $("#id_company").remove();
        $("label[for='id_company']").remove();
    }
    else if ($("#is_engineer").length > 0) {
        $("#id_university").remove();
        $("label[for='id_university']").remove();
    }
    else {
        $("#id_almamater").remove();
        $("label[for='id_almamater']").remove();
        $("#id_about").remove();
        $("label[for='id_about']").remove();
        $("#id_company").remove();
        $("label[for='id_company']").remove();
        $("#id_university").remove();
        $("label[for='id_university']").remove();
    }
});