
$(document).ready(function() {
    $('#servicoSelect1').change(function() {
        var selectedServiceId = $(this).val();
        
        
        if (selectedServiceId) {
            obter_horario(selectedServiceId, function(hora_inicio, hora_pausa, hora_retomada, hora_final) {
                $('#hora_inicio').val(hora_inicio);
                $('#hora_pausa').val(hora_pausa);
                $('#hora_retomada').val(hora_retomada);
                $('#hora_final').val(hora_final); 
                $('#ConfigContainer').show();
            });
        } else {
            $('#ConfigContainer').hide();
        }
    });
});

$(document).ready(function() {
    $('#servicoSelect2').change(function() {
        var selectedServiceId = $(this).val();
        
        if (selectedServiceId) {
            obter_tempo_atendimento(selectedServiceId, function(tempo_atendimento) {
                $('#tempoAtendimento').val(tempo_atendimento);
                $('#tempoAtendimentoContainer').show();
            });
        } else {
            $('#tempoAtendimentoContainer').hide();
        }
    });
});

function obter_horario(selectedServiceId, callback) {
    var csrfToken = $('input[name=csrf_token]').val();

    

    // Faz uma requisição AJAX para obter os horários disponíveis, incluindo o token CSRF
    $.ajax({
        type: 'POST',
        url: '/api/obter_horario',
        contentType: 'application/json',
        data: JSON.stringify({ 'servico_id': selectedServiceId}),
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: function(data) {
            
            var hora_inicio = data.hora_inicio
            var hora_pausa = data.hora_pausa
            var hora_retomada = data.hora_retomada
            var hora_final = data.hora_final

            if (callback) {
                callback(hora_inicio, hora_pausa, hora_retomada, hora_final);
            }
        },
        error: function(error) {
        
            console.error('Erro ao obter o horário de funcionamento', error);
        }
    });
}

function obter_tempo_atendimento(selectedServiceId, callback) {
    var csrfToken = $('input[name=csrf_token]').val();

    

    // Faz uma requisição AJAX para obter os horários disponíveis, incluindo o token CSRF
    $.ajax({
        type: 'POST',
        url: '/api/obter_tempo_atendimento',
        contentType: 'application/json',
        data: JSON.stringify({ 'servico_id': selectedServiceId}),
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: function(data) {
        
            var tempo_atendimento = data.tempo_atendimento

            if (callback) {
                callback(tempo_atendimento);
            }
        },
        error: function(error) {
        
            console.error('Erro ao obter o tempo do atendimento', error);
        }
    });
}