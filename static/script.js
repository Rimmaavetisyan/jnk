document.addEventListener("DOMContentLoaded", function () {
    const flashMessages = document.querySelectorAll(".flash-message");
    setTimeout(() => {
        flashMessages.forEach(msg => msg.style.display = "none");
    }, 4000);
});
