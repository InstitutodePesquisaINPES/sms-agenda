var changedValue = false // Variavel de escopo global para ser acessada pelas funções de prev e next steps
var diasDesativados = []
var horas_disponiveis = []

// API PARA AS BUSCAS DAS DATAS DISPONIVEIS (CUIDADO AO MEXER)
document.addEventListener('DOMContentLoaded', function () {
    // Fazer uma requisição AJAX para obter os dados dos agendamentos por dia
    fetch('/api/agendamentos_por_dia')
        .then(response => response.json())
        .then(dias_list => {
            // Agora 'dias_list' contém os dados dos agendamentos por dia
            console.log(dias_list);

            diasDesativados = dias_list

            console.log(diasDesativados)

            
        })
        .catch(error => console.error('Erro ao obter dados dos agendamentos por dia:', error));
});

function obterHorariosDisponiveis() {
    var dataSelecionada = document.getElementById('datePicker').value;

    var csrfToken = $('input[name=csrf_token]').val();

    console.log(dataSelecionada)

    // Faz uma requisição AJAX para obter os horários disponíveis, incluindo o token CSRF
    $.ajax({
        type: 'POST',
        url: '/api/horarios_disponiveis',
        contentType: 'application/json',
        data: JSON.stringify({ 'data_selecionada': dataSelecionada }),
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: function(data) {
            // Renderiza os horários disponíveis no frontend
            console.log(data.horarios_disponiveis)
            renderizarHorarios(data.horarios_disponiveis);
        },
        error: function(error) {
            console.error('Erro ao obter horários disponíveis:', error);
        }
    });
}

function renderizarHorarios(horarios) {
    var divHorarios = document.getElementById('divHorarios');
    divHorarios.innerHTML = '';  // Limpa a div antes de renderizar os novos horários

    var titulo = document.createElement('h2');
    titulo.textContent = 'Escolha seu horário';
    titulo.className = 'hora-title subtitle-formAgendamento'
    divHorarios.appendChild(titulo);

    // Renderiza os horários disponíveis como radio buttons
    horarios.forEach(function(hora) {
        var divContainer = document.createElement('div-withHoras');
        divContainer.className = 'form-check form-check-inline';

        var inputRadio = document.createElement('input');
        inputRadio.type = 'radio';
        inputRadio.name = 'hora_ipt';
        inputRadio.className = 'input-hora form-check-input';
        inputRadio.value = hora;

        var label = document.createElement('label');
        label.className = 'form-check-label'
        label.textContent = hora;

        divContainer.appendChild(inputRadio);
        divContainer.appendChild(label);
        divHorarios.appendChild(divContainer);
    });
}

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

function dadosParaModal() {
    // Supondo que você tenha lógica para obter os valores selecionados do datePicker e dos radio buttons
    var diaSelecionado = document.getElementById('datePicker').value;
    // var horaSelecionada = document.querySelector('input[name="hora"]:checked').value;

    // Atualize os parágrafos no modal com os valores selecionados
    document.getElementById('diaAgendado').textContent = diaSelecionado;
    // document.getElementById('horaAgendada').textContent = horaSelecionada;
}

document.getElementById('btnSalvarAgenda').addEventListener('click', function () {
    dadosParaModal();
});
