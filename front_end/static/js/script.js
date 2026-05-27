

const openMenu = document.getElementById("openMenu");
const closeMenu = document.getElementById("closeMenu");
const links = document.querySelectorAll("a");

openMenu.addEventListener("click", () => {
    menu.classList.add("ativo");
});

closeMenu.addEventListener("click", () => {
    menu.classList.remove("ativo");
});

menu.addEventListener("click", () => {
    menu.classList.remove("ativo");
});


