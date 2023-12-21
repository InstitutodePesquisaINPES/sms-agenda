// Seu código JavaScript aqui
$(document).ready(function() {
    $('#servicoSelect').change(function() {
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

function obter_tempo_atendimento(selectedServiceId, callback) {
    var csrfToken = $('input[name=csrf_token]').val();

    console.log(selectedServiceId) 

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
            console.log(tempo_atendimento)

            if (callback) {
                callback(tempo_atendimento);
            }
        },
        error: function(error) {
        
            console.error('Erro ao obter o tempo do atendimento', error);
        }
    });
}