$(document).ready(function(){
    $("#btn-regist").click(function() {
        $(".divform").css("display","none");
        $(".divform2").css("display","inline");
    });
    $("#btn-enviar").click(function() {
        $("#fg2").submit(function(event) {
            if ($("#usr2").val() == "" || $("#pass2").val() == "") {
                event.preventDefault();
            }
        });
    });
});