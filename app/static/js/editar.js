$(document).ready(function () {
    console.log("func1")
    // Quando o botão de salvar for clicado
    $("#botao_salvar_editar").on("click", function () {
        console.log("func2")
        // Obter o valor do campo 'status'
        var statusValue = $("#status").val();
        console.log("func3")
        // Verificar se o status é "Retificado"
        if (statusValue == "retificado") {
            // Se sim, mostrar o segundo modal
            console.log("func4")
            $("#modalRetificacao").modal("show");
        } else {
            // Se não, enviar o formulário normalmente
            console.log("func1")
            $("form").submit();

        }
    });
});

function enviarComRetificacao() {
    // Adicione aqui qualquer lógica adicional antes de enviar o formulário
    // ...

    // Enviar o formulário
    $("form").submit();

    // Fechar o segundo modal
    $("#modalRetificacao").modal("hide");
}