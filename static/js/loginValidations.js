(() => {
    var form = document.getElementById("fg2");
    var email = document.getElementById("email");
    var passwd = document.getElementById("pass2");
    var select = document.getElementById("sel1");
    var err = [];
    window.onload = function () {
        function hide() {
            document.getElementById("alert").style.transform = "translateY(100px);"
            document.getElementById("alert").style.transition = "all 0.2s ease";
            document.getElementById("alert").style.display = "none";
        }
        function errors() {
            var errs = "";
            for (var x = 0; x < err.length; x++) {
                errs += "<span>"+ (x + 1) + ". " + (err[x]) + "</span>" + "<br>";
            }
            document.getElementById("alert").innerHTML = "<span class='err'>¡Error!</span><br>" + errs;
            document.getElementById("alert").style.display = "inherit";
            // window.scrollTo(0,0);
            const tout = setTimeout(hide, 8000);
            err.splice(0,err.length);
        }
        function emailValid(email) {
            // patron = /^[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/;
            patron = /^[a-zA-Z0-9]+(?:\.[a-z0-9]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/;
            var valid = patron.test(email);
            if (valid == true) {
                return
            } else {
                err.push("Por favor introduzca un <strong>Email</strong> válido.");
            }
        }
        function passwdValid(passwd) {
            patron = /^(?=.*\d)(?=.*[*$&-/!#])(?=.*[a-z]).*[A-Z]/;
            if (passwd.length < 8) {
                err.push("Por favor introduce una <strong>contraseña</strong> válida:<br>- Debe ser mayor a 8 caracteres.<br>- Debe contener al menos 1 mayúscula.<br>- Debe contener al menos 1 minúscula.<br>- Debe contener al menos 1 dígito.<br>- Debe contener al menos 1 caracter especial.<br> Los carácteres especiales aceptados son: *$&-/!#");
            } else if (!patron.test(passwd)) {
                err.push("Por favor introduce una <strong>contraseña</strong> válida:<br>- Debe ser mayor a 8 caracteres.<br>- Debe contener al menos 1 mayúscula.<br>- Debe contener al menos 1 minúscula.<br>- Debe contener al menos 1 dígito.<br>- Debe contener al menos 1 caracter especial.<br> Los carácteres especiales aceptados son: *$&-/!#");
            }
        }
        form.onsubmit = () => {
            //condicionales para el select rol
            if (select.value.trim() == "") {
                err.push("Por favor no deje el campo <strong>Select</strong> vacío.");
            }
            //condicionales para el campo email
            if (email.value.trim() == "") {
                err.push("Por favor no deje el campo <strong>Email</strong> vacío.");
            } else {
                emailValid(email.value);
            }
            //condicionales para el campo Nombre
            if (passwd.value.trim() == "") {
                err.push("Por favor no deje el campo <strong>Contraseña</strong> vacío.");
            } else {
                passwdValid(passwd.value)
            }
            if (err.length > 0) {
                event.preventDefault();
                errors();
            }
        }
    }
})();