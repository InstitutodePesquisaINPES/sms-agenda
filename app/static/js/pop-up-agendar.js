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

// API PARA BUSCA DAS HORAS, CONFORME A DATA SELECIONADA (CUIDADO AO MEXER)
document.getElementById('confirmData').addEventListener('click', function () {
    
    selectedDate = document.getElementById("datePicker").value;

    // Fazer uma requisição AJAX para obter os dados dos horarios disponiveis
    fetch('/api/horarios_disponiveis', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data: dataDesejada })
    })
    .then(response => response.json())
    .then(horas_list => {
        // agora horas_list tem os dados das horas disponiveis
        horas_disponiveis = horas_list
        console.log(horas_disponiveis);

        
    })
    .catch(error => console.error('Erro ao obter dados dos horarios disponiveis neste dia:', error));
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

// Obtém o elemento do formulário
const div_horas = document.getElementById('div-hora');

// Itera sobre a lista e cria botões de rádio
minhaLista.forEach(function (opcao, indice) {
  // Cria um elemento de input radio
  const inputRadio = document.createElement('input');
  inputRadio.type = 'radio';
  inputRadio.name = 'opcoes'; // Certifique-se de dar o mesmo nome para agrupar os botões
  inputRadio.value = opcao;

  // Cria uma label para o botão de rádio
  const label = document.createElement('label');
  label.textContent = opcao;

  // Adiciona o input radio e a label ao formulário
  div_horas.appendChild(inputRadio);
  div_horas.appendChild(label);

  // Adiciona uma quebra de linha para melhorar a visualização
  div_horas.appendChild(document.createElement('br'));
});
