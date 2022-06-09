(() => {
    window.onload = function() {
        var btn = document.querySelector(".menu-icon");
        var menu = document.querySelector("#tog");
        btn.onclick = function() {
            menu.classList.toggle("hide")
            menu.classList.toggle("shown")
        };
        window.addEventListener("scroll", function() {
            var header = document.querySelector("header");
            header.classList.toggle("sticky", window.scrollY > 0);
        })
    }
})();