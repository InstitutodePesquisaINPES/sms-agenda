console.log("Script carregado!");

document.addEventListener("DOMContentLoaded", function () {
    var flashMessages = document.querySelectorAll('.flash');

    flashMessages.forEach(function (flashMessage) {
        var messageText = flashMessage.textContent;
        var category = flashMessage.classList[1];

        if (category === 'flash-success') {
            flashMessage.innerHTML = '<i class="bi bi-check-circle-fill"></i> ' + messageText;
            console.log("Sucesso!");
        } else if (category === 'flash-error') {
            flashMessage.style.backgroundColor = '#e74c3c';
            flashMessage.style.color = 'white';
            flashMessage.innerHTML = '<i class="fas fa-exclamation-circle"></i> ' + messageText;
        }
    });
});