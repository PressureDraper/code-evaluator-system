function eml(e) {
    let key = e.which;

    // Patron de entrada, en este caso solo acepta numeros, letras, . y @
    let patron = /[a-zA-Z0-9@\.]/;
    let final_key = String.fromCharCode(key);
    return patron.test(final_key);
}