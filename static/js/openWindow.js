function changeDisplay() {
    $("#blurdiv").css("display", "block");
}

let close = document.getElementById("close");

close.onclick = () => {
    $("#blurdiv").css("display", "none");
}