var changedValue = false // Variavel de escopo global para ser acessada pelas funções de prev e next steps
var diasDesativados = []
var horas_disponiveis = []

// API PARA AS BUSCAS DAS DATAS DISPONIVEIS (CUIDADO AO MEXER)
document.addEventListener('DOMContentLoaded', function () {
    var id_servico = document.getElementById('id_servico').value;
    console.log(id_servico)
    var csrfToken = $('input[name=csrf_token]').val();
    
    // Fazer uma requisição AJAX para obter os dados dos agendamentos por dia
    $.ajax({
        type: 'POST',
        url: '/api/agendamentos_por_dia',
        contentType: 'application/json',
        data: JSON.stringify({'servico_id': id_servico}),
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: function(data) {
            lista_datas = data.dias_list
            for (var i = 0; i < lista_datas.length; i++) {
                diasDesativados.push(String(lista_datas[i]));
            }
            
            FunctDatePicker()
            
        },
        error: function(error) {
        
            console.error('Erro ao obter horários disponíveis:', error);
            
        }
    });
});

function obterHorariosDisponiveis() {
    var dataSelecionada = document.getElementById('datePicker').value;

    var csrfToken = $('input[name=csrf_token]').val();

    var id_servico = document.getElementById('id_servico').value;


    // Faz uma requisição AJAX para obter os horários disponíveis, incluindo o token CSRF
    $.ajax({
        type: 'POST',
        url: '/api/horarios_disponiveis',
        contentType: 'application/json',
        data: JSON.stringify({ 'data_selecionada': dataSelecionada, 'servico': id_servico}),
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

    var titulo = document.createElement('p');
    divHorarios.appendChild(titulo);

    var divContainer = document.createElement('div');
    divContainer.className = 'horarios-container';

    // Renderiza os horários disponíveis como radio buttons
    horarios.forEach(function(hora, index) {
        var inputRadio = document.createElement('input');
        inputRadio.type = 'radio';
        inputRadio.name = 'hora_ipt';
        inputRadio.className = 'input-hora form-check-input';
        inputRadio.id = 'hora_' + hora.replace(':', ''); // Adiciona um ID único baseado na hora
        inputRadio.value = hora;

        var label = document.createElement('label');
        label.className = 'form-check-label';
        label.setAttribute('for', 'hora_' + hora.replace(':', '')); // Associa o label ao input
        label.innerHTML = hora + ' <i class="bi bi-check"></i>';

        var divItem = document.createElement('div');
        divItem.className = 'form-check';
        divItem.appendChild(inputRadio);
        divItem.appendChild(label);

        divContainer.appendChild(divItem);

        // Adiciona a divContainer à divHorarios e reinicia a cada 4 elementos
        if ((index + 1) % 4 === 0 || index === horarios.length - 1) {
            divHorarios.appendChild(divContainer);
            divContainer = document.createElement('div');
            divContainer.className = 'horarios-container';
        }
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
            }
        ]
    });
});
// document.addEventListener('DOMContentLoaded', function() {

//     console.log(diasDesativados),
//     // Inicialize o Flatpickr
//     flatpickr("#datePicker", {
//         dateFormat: "Y-m-d", // Formato da data
//         minDate: "today",    // Define a data mínima como hoje
//         maxDate: new Date().fp_incr(29),  // Define a data máxima como 30 dias a partir de hoje
//         disableMobile: "true", // Desativa o seletor nativo em dispositivos móveis
//         inline: true, // exibe o calendario inline
//         disable: [
//             function(date) {
//                 // Desativa sábados e domingos
//                 if (date.getDay() === 0 || date.getDay() === 6) {
//                     return true;
//                 }

//                 // // Desativa os dias 15 e 25 de cada mês
//                 // if (date.getDate() === 15 || date.getDate() === 25) {
//                 //     return true;
//                 // }

//                 var dataAtual = date.getDate()

//                 if(diasDesativados.includes(dataAtual)){
//                     return true;
//                 }
                
//                 // Mantém os outros dias habilitados
//                 return false;
//             }
//         ]

//     });
// });

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
                var upload = $("#upload\\?").val();
                let checkbox1 = $("input[name='i-confirm']").is(":checked");
                let checkbox2 = $("input[name='li']").is(":checked");
                if(upload == "True"){
                    if(documentosEnviados.length > 0){
                        if (checkbox1 && checkbox2) {
                            
                            return true
                        }
                    }
                }else{
                    if (checkbox1 && checkbox2) {
                            
                        return true
                    }
                }
            }
        }

        return false;
    }
});

// Código para puxar a data do calendar 
function FunctDatePicker() {
    // Obter a data atual
    var dataAtual = new Date();
    var diaAtual = dataAtual.getDate();
    var mesAtual = dataAtual.getMonth() + 1; // Mês começa do zero, então adicionamos 1
    var anoAtual = dataAtual.getFullYear();
    var nomeDiaSemanaAtual = dataAtual.toLocaleDateString('pt-BR', { weekday: 'long' });
    var nomeMesAtual = dataAtual.toLocaleDateString('pt-BR', { month: 'long' });

    // Enviando os elementos para o HTML na carga inicial
    var daySelectCalendar = document.querySelector(".getCalendarDay");
    var dayBackSelectCalendar = document.querySelector(".getCalendarDayBackground");
    var daySelectCalendarDescript = document.querySelector(".getCalendarDayDescription");
    var dayBackSelectCalendarDescript = document.querySelector(".getCalendarYearBackground");
    var monthSelectCalendar = document.querySelector(".getCalendarMonth");
    var getSelectCalendar = document.querySelector(".getCalendarYear");

    daySelectCalendar.innerText = diaAtual;
    dayBackSelectCalendar.innerText = diaAtual;  // Atualizado
    daySelectCalendarDescript.innerText = nomeDiaSemanaAtual;
    dayBackSelectCalendarDescript.innerText = nomeDiaSemanaAtual;  // Atualizado
    monthSelectCalendar.innerText = nomeMesAtual;
    getSelectCalendar.innerText = anoAtual;


    // Inicialize o Flatpickr
    flatpickr("#datePicker", {
        dateFormat: "Y-m-d",
        minDate: "today",
        maxDate: new Date().fp_incr(29),
        disableMobile: "true",
        inline: true,
        disable: [
            function(date) {
                // Desativa sábados e domingos
                if (date.getDay() === 0 || date.getDay() === 6) {
                    return true;
                }

                function adicionarZero(numero) {
                    if (numero < 10) {
                        return '0' + numero;
                    }
                    return numero;
                }


                var dataAtualdt = adicionarZero(date.getDate());
                
                
                var mesAtualdt = adicionarZero(date.getMonth() + 1);
                var anoAtualdt = date.getFullYear()

                
                //console.log(anoAtualdt,mesAtualdt, dataAtualdt);

                // montar string data

                data_atualdt = anoAtualdt + "-" + mesAtualdt + "-" + dataAtualdt                 

                console.log(data_atualdt)
                console.log(diasDesativados)
                console.log("desativado A")

                

                if(diasDesativados.includes(String(data_atualdt))){
                     console.log('funcionou')
                     return true
                }
            }

        ],
        
        onChange: function(selectedDates, dateStr, instance) {

            // Aqui você obtém o valor do dia, mês e ano selecionados e exibe no console
            if (selectedDates.length > 0) {
                var dataSelecionada = selectedDates[0];
                
                var diaSelecionado = dataSelecionada.getDate();
                var mesSelecionado = dataSelecionada.getMonth() + 1;
                var anoSelecionado = dataSelecionada.getFullYear();

                // Obtenha o nome do dia da semana e do mês
                var nomeDiaSemana = dataSelecionada.toLocaleDateString('pt-BR', { weekday: 'long' });
                var nomeMes = dataSelecionada.toLocaleDateString('pt-BR', { month: 'long' });

                // Enviando os elementos para o HTML
                daySelectCalendar.innerText = diaSelecionado;
                dayBackSelectCalendar.innerText = diaSelecionado;
                daySelectCalendarDescript.innerText = nomeDiaSemana;
                dayBackSelectCalendarDescript.innerText = nomeDiaSemana;
                monthSelectCalendar.innerText = nomeMes;
                getSelectCalendar.innerText = anoSelecionado;
            }
        }
    });


    // ... seu código existente
};

// function verificaCondicional(data) {
//     // Extrai ano, mês e dia da data fornecida
//     var partesData = data.split("-");
//     var anoAtualdt = parseInt(partesData[0]);
//     var mesAtualdt = parseInt(partesData[1]);
//     var diaAtualdt = parseInt(partesData[2]);

//     // Condição a ser verificada
//     if (mesAtualdt === 12 && anoAtualdt === 2023 && diaAtualdt === 27) {
//         return true;
//     }

    //return false;
//}

// function handleFileChange(){
//     var fileInput = document.getElementById('updoc');
//     var file = fileInput.files[0];

//     // Verifica se um arquivo foi selecionado
//     if (!file) {
//         alert('Selecione um arquivo.');
//         return;
//     }

//     // Verifica a extensão do arquivo
//     var allowedExtensions = ['jpg', 'jpeg','.pdf'];
//     var fileExtension = file.name.split('.').pop().toLowerCase();

//     if (allowedExtensions.indexOf(fileExtension) === -1) {
//         alert('Tipo de arquivo não permitido. Selecione um arquivo com extensão: ' + allowedExtensions.join(', '));

//         // Limpa o campo de arquivo
//         fileInput.value = '';
//         return;
//     }

//     // Continue com o processamento do arquivo, se necessário
//     // Você pode adicionar lógica adicional aqui, se desejar
// }