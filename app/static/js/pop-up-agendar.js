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
            

            diasDesativados = dias_list

            

            
        })
        .catch(error => console.error('Erro ao obter dados dos agendamentos por dia:', error));
});

function obterHorariosDisponiveis() {
    var dataSelecionada = document.getElementById('datePicker').value;

    var csrfToken = $('input[name=csrf_token]').val();

    

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
    
    var diaSelecionado = document.getElementById('datePicker').value;
    var horaSelecionada = document.querySelector('input[name="hora_ipt"]:checked').value;

    var dataBrasileira = converte_data_americana(diaSelecionado);
    var horaFormatada = formatarHora(horaSelecionada);

    document.getElementById('diaAgendado').textContent = dataBrasileira;
    document.getElementById('horaAgendada').textContent = horaFormatada;
}

document.getElementById('btnSalvarAgenda').addEventListener('click', function () {
    dadosParaModal();
});

function converte_data_americana(data){

    // Dividir a data em pedaços
    var partes = data.split('-');
    var ano = partes[0];
    var mes = partes[1];
    var dia = partes[2];

    // Formata a data
    var diaFormatado = dia.padStart(2, '0');
    var mesFormatado = (mes).toString().padStart(2, '0');
    var anoFormatado = ano;

    var dataFormatada = `${diaFormatado}-${mesFormatado}-${anoFormatado}`;

    return dataFormatada
}

function formatarHora(horaString) {
    // Dividir a string em horas e minutos
    const [horas, minutos] = horaString.split(':');
  
    // Formatar a string no novo formato
    const horaFormatada = `${horas}h${minutos}min`;
  
    return horaFormatada;
}

$(document).ready(function () {
    // Evento de clique do botão "SALVAR"
    $("#btnSalvarAgenda").click(function () {
        // Verifique se a data, hora, pelo menos um documento e ambos os checkboxes estão marcados
        if (validarAgendamento()) {
            // Abra o modal programaticamente
            $("#meuModal").modal("show");
        } else {

            // verifica se o erro é os checkbox
            let checkbox1 = $("input[name='i-confirm']").is(":checked");
            let checkbox2 = $("input[name='li']").is(":checked");
            if (!checkbox1 || !checkbox2) {
                alert("Por favor, confirme se tem consentimento do agendamento e dos documentos necessários e marque as opções abaixo antes de continuar.")         
            } else {
                // Caso contrário, exiba uma mensagem de erro ou tome outra ação necessária
                alert("Por favor, preencha todos os campos necessários.");
            }
            
        }
    });

    function validarAgendamento() {
        let dataSelecionada = $("#datePicker").val();
        if(dataSelecionada != ""){
            
            let radioSelecionado = $("input[name='hora_ipt']").is(":checked");
            if(radioSelecionado){
                
                let documentosEnviados = $("#updoc").prop("files");
                if(documentosEnviados.length > 0){
                    
                    let checkbox1 = $("input[name='i-confirm']").is(":checked");
                    let checkbox2 = $("input[name='li']").is(":checked");
                    if (checkbox1 && checkbox2) {
                        
                        return true
                    }
                }
            }
        }

        return false;
    }
});
