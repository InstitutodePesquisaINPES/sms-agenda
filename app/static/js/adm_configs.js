$(document).ready( function() {
    $('#servicoSelect1').change(function(){
        var selectedServiceId = $(this).val();
        $('#diaSelect1').change(function(){
            var selectedDay = $(this).val();
            if(selectedDay && selectedServiceId){
                
                obter_horario_e_tempo(selectedDay, selectedServiceId, function(hora_inicio, hora_pausa, hora_retomada, hora_final, tempo_atendimento){
                    $('#hora_inicio').val(hora_inicio);
                    $('#hora_pausa').val(hora_pausa);
                    $('#hora_retomada').val(hora_retomada);
                    $('#hora_final').val(hora_final);
                    $('#tempo_atendimento').val(tempo_atendimento);
                    $('#ConfigContainer').show();
                });
            } else {
                $('#ConfigContainer').hide();
            }
        })
    })
})

function obter_horario_e_tempo(selectedDay, selectedServiceId, callback) {
    var csrfToken = $('input[name=csrf_token]').val();
    // Faz uma requisição AJAX para obter os horários disponíveis, incluindo o token CSRF
    $.ajax({
        type: 'POST',
        url: '/api/obter_horario_e_tempo_atendimento',
        contentType: 'application/json',
        data: JSON.stringify({ 'servico_id': selectedServiceId, 'dia_semana': selectedDay}),
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: function(data) {
            
            var hora_inicio = data.hora_inicio
            var hora_pausa = data.hora_pausa
            var hora_retomada = data.hora_retomada
            var hora_final = data.hora_final
            var tempo_atendimento = data.tempo_atendimento

            if (callback) {
                callback(hora_inicio, hora_pausa, hora_retomada, hora_final, tempo_atendimento);
            }
        },
        error: function(error) {
        
            console.error('Erro ao obter o horário de funcionamento', error);
        }
    });
}