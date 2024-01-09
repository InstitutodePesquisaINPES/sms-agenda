from urllib.parse import quote
import webbrowser
import pyautogui
import time
import os

def enviar_mensagem_whatsapp( telefone, mensagem):
    link_zap = f'https://web.whatsapp.com/send?phone={telefone}&text={quote(mensagem)}'

    try:
        webbrowser.open_new_tab(link_zap)

        # Aguarda até que a imagem 'seta2.png' seja encontrada ou até um timeout de 60 segundos
        timeout = 60
        start_time = time.time()
        seta = None 
        # Obtendo o diretório do script
        diretorio_script = os.path.dirname(__file__)

        # Construindo o caminho para o arquivo desejado
        caminho_do_icone = os.path.join(diretorio_script, '../../app/static/assets/icons/seta2.png')

        while seta is None and time.time() - start_time < timeout:
            seta = pyautogui.locateCenterOnScreen(caminho_do_icone)

            if seta is None:
                time.sleep(1)  # Aguarde 1 segundo antes de tentar novamente

        if seta is not None:
            pyautogui.click(seta[0], seta[1])
        else:
            print("Imagem não encontrada ou timeout atingido.")
        print('fechar')
        time.sleep(10)
        pyautogui.hotkey('ctrl', 'w')

        return 'enviado'
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")
        return 'falhou'

