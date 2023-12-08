var changedValue = false // Variavel de escopo global para ser acessada pelas funções de prev e next steps
var diasDesativados = []


function changed(boolean){ // saber se o usúario inseriu algum dado antes de avançar e etapa, passa esta função no onChange""
    changedValue = boolean
}

document.getElementById('open-popup').addEventListener('click', function() {
    showStep(1); // Certifique-se de que o primeiro passo esteja visível ao abrir o pop-up
    showPopup();
});

function showPopup() {
    var popup = document.getElementById('popup');
    var closePopupButton = document.getElementById('close-popup');
    popup.style.display = 'block';
    closePopupButton.style.display = 'block';

    // Limpar os dados dos inputs quando o pop-up é aberto
    clearForm();
}

function closePopup() {
    var popup = document.getElementById('popup');
    var closePopupButton = document.getElementById('close-popup');
    popup.style.display = 'none';
    closePopupButton.style.display = 'none';

    // Limpar os dados dos inputs quando o pop-up é fechado
    clearForm();
}

// Função para limpar os dados dos inputs
function clearForm() {
    var inputs = document.querySelectorAll('.popup-content input');
    inputs.forEach(function(input) {
        // Verifica se o tipo do input é "checkbox" para desmarcá-lo
        if (input.type === 'checkbox') {
            input.checked = false;
        } else {
            input.value = ''; // Limpa o valor dos outros tipos de input
        }
    });
}

// Função para avançar para o próximo passo
function nextStep() {
    var currentStep = getCurrentStep();

    if(changedValue){
        changed(false); // retorna valor inicial a variável global

        // Lógica para verificar em qual passo estamos
        if (currentStep === 1) {
            // Lógica específica para o passo 1
            var checkboxChecked = document.querySelector('#step1 input[name="checkbox"]').checked;
            if (!checkboxChecked) {
                alert('Por favor, confirme que leu e possui todos os documentos necessários.');
                return;
            }
        } else if (currentStep === 2) {
            // Lógica específica para o passo 2
            // Você pode adicionar lógica adicional aqui, se necessário
        } else if (currentStep === 3) {
            // Lógica específica para o passo 3
            // Você pode adicionar lógica adicional aqui, se necessário
        } else if (currentStep === 4) {
            // Lógica específica para o passo 4
            // Você pode adicionar lógica adicional aqui, se necessário
        }

        // Avance para o próximo passo
        showStep(currentStep + 1);

        // Adicione lógica para avançar para o próximo passo
        selectedDate = document.getElementById("datePicker").value;
        radios = document.getElementsByName('hora_ipt');

        var selectedTime

        for(var i = 0; i < radios.length; i++){
            if(radios[i].checked){
                selectedTime = radios[i].value;
                break 
            }
        }

        console.log(selectedDate);
        console.log(selectedTime);

        // Atualize os valores dos campos ocultos
        document.getElementById("data_selecionada").value = selectedDate;
        document.getElementById("hora_selecionada").value = selectedTime;

        var dataElement = document.getElementById("data-sel");
        var horaElement = document.getElementById("hora-sel");

        document.getElementById("selected-date").value = selectedDate;
        document.getElementById("selected-time").value = selectedTime;

        dataElement.innerHTML = selectedDate;
        horaElement.innerHTML = selectedTime;
    }
}


// Função para voltar para o passo anterior
function prevStep() {
    var currentStep = getCurrentStep();

    // Volte para o passo anterior
    showStep(currentStep - 1);
}

// Função auxiliar para mostrar um passo específico
function showStep(stepNumber) {
    var steps = document.querySelectorAll('.popup-content');
    for (var i = 0; i < steps.length; i++) {
        steps[i].style.display = i + 1 === stepNumber ? 'block' : 'none';
    }
}

// Função auxiliar para obter o número do passo atual
function getCurrentStep() {
    var steps = document.querySelectorAll('.popup-content');
    for (var i = 0; i < steps.length; i++) {
        if (steps[i].style.display !== 'none') {
            return i + 1;
        }
    }
    return 1; // Se nenhum passo estiver visível, assuma o primeiro passo
}

function submitForm() {
    window.location.href = "meusagendamentos"
    closePopup();
}

document.addEventListener('DOMContentLoaded', function () {
    // Fazer uma requisição AJAX para obter os dados dos agendamentos por dia
    fetch('/api/agendamentos_por_dia')
        .then(response => response.json())
        .then(dias_list => {
            // Agora 'data' contém os dados dos agendamentos por dia
            console.log(dias_list);

            diasDesativados = dias_list

            console.log(diasDesativados)

            
        })
        .catch(error => console.error('Erro ao obter dados dos agendamentos por dia:', error));
});

document.addEventListener('DOMContentLoaded', function() {
    // Inicialize o Flatpickr
    flatpickr("#datePicker", {
        dateFormat: "Y-m-d", // Formato da data
        minDate: "today",    // Define a data mínima como hoje
        maxDate: new Date().fp_incr(29),  // Define a data máxima como 30 dias a partir de hoje
        disableMobile: "true", // Desativa o seletor nativo em dispositivos móveis
        inline: true, // exibe o calendario inline
        disable: [
            function(date) {
                // Desativa sábados e domingos
                if (date.getDay() === 0 || date.getDay() === 6) {
                    return true;
                }

                // Desativa os dias 15 e 25 de cada mês
                if (date.getDate() === 15 || date.getDate() === 25) {
                    return true;
                }

                var dataAtual = date.getDate()

                if(diasDesativados.includes(dataAtual)){
                    return true;
                }
                
                // Mantém os outros dias habilitados
                return false;
            }
        ]

    });
});
