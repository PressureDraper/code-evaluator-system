function sqliname(e) {
    let key = e.which;

    // Patron de entrada, en este caso solo acepta numeros y letras
    let patron = /^[A-Za-z ]*$/;
    let final_key = String.fromCharCode(key);
    return patron.test(final_key);
}