document.addEventListener('DOMContentLoaded', function () {
    // Adicione um ouvinte de evento para o botão de retificação
    console.log("func1")
    document.getElementById('botao_salvar_editar').addEventListener('click', function () {
        // Verifica se a opção selecionada é "retificado"
        console.log("func2")
        if (document.getElementById('status_admin').value === 'retificado') {
            // Exibe o modal de retificação
            $('#retificacaoModal').modal('show');
            console.log("func3")

        } else {
            // Se não for "retificado", fecha o modal de retificação (caso esteja aberto)
            $('#retificacaoModal').modal('hide');
            console.log("func4")
            
            // Envie o formulário diretamente
            document.getElementById('form-editar').submit();
        }
    });

    // Adicione um ouvinte de evento para o botão de confirmar retificação
    document.getElementById('botao_confirmar_retificacao').addEventListener('click', function () {
        // Adicione aqui a lógica para salvar a retificação, se necessário
        // ...
        console.log("func5")
        // Fecha o modal de retificação
        

        // Envie o formulário ao clicar no botão de confirmar no modal da retificação
        document.getElementById('form-editar').submit();
    });

    // // Adicione um ouvinte de evento para o botão de salvar
    // document.getElementById('botao_salvar_editar').addEventListener('click', function () {
    //     // Adicione aqui a lógica para salvar os dados, se necessário
    //     // ...

    //     // Envie o formulário
    //     document.getElementById('form-editar').submit();
    // });
});
