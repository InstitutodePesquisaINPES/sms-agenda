// Seu código JavaScript aqui
$(document).ready(function() {
    $('#servicoSelect').change(function() {
        var selectedServiceId = $(this).val();
        
        if (selectedServiceId) {
            var selectedService = servicos[selectedServiceId];
            $('#tempoAtendimento').val(selectedService.tempo_atendimento);
            $('#tempoAtendimentoContainer').show();
        } else {
            $('#tempoAtendimentoContainer').hide();
        }
    });
});
