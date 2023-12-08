document.addEventListener('DOMContentLoaded', function() {
    // Inicialize o Flatpickr
    flatpickr("#datePicker", {
        dateFormat: "Y-m-d", // Formato da data
        minDate: "today",    // Define a data mínima como hoje
        maxDate: new Date().fp_incr(30),  // Define a data máxima como 30 dias a partir de hoje
        disableMobile: "true", // Desativa o seletor nativo em dispositivos móveis
        inline: true, // exibe o calendario inline
    });
});