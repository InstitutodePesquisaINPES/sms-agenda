from app.models.model_user import *

def paraMinutos(hora):
    emMinutos = hora.hour * 60 + hora.minute
    return emMinutos

def calculaHoras(): # puxa do banco a quantidade de horas de cada horario de atendimento, util na api do calendario
    
    # e `hora_inicio` e `hora_pausa` são campos no seu modelo
    horario1 = Horarios_disponiveis.query.filter_by(id=1).first()

    # Certifique-se de que `hora_inicio` e `hora_pausa` sejam objetos time
    hora_inicio = horario1.hora_inicio
    hora_pausa = horario1.hora_pausa
    tempo_pausa = horario1.tempo_pausa
    hora_retomada = horario1.hora_retomada
    hora_final = horario1.hora_final
    tempo_atendimento = horario1.tempo_atendimento

    # Converta os objetos time para representações numéricas (por exemplo, minutos)
    minutos_inicio = paraMinutos(hora_inicio)
    minutos_pausa = paraMinutos(hora_pausa)
    minutos_pausados = paraMinutos(tempo_pausa)
    minutos_retomada = paraMinutos(hora_retomada)
    minutos_final = paraMinutos(hora_final)
    minutos_atendimento = paraMinutos(tempo_atendimento)

    # Calcula a diferença entre os minutos
    manhaMinutos = minutos_pausa - minutos_inicio
    tardeMinutos = minutos_final - minutos_retomada

    qntManha = manhaMinutos / minutos_atendimento
    qntTarde = tardeMinutos / minutos_atendimento

    # Se necessário, manipule diferença_em_minutos de acordo com suas necessidades
    return qntManha + qntTarde #retorna 2 em cada

    # soma do return da 4, usar um count com filtro por dia, para saber quantos agendamentos tem no dia pra saber se ta disponivel 
 
def calculaHorarios():
    # e `hora_inicio` e `hora_pausa` são campos no seu modelo
    horario1 = Horarios_disponiveis.query.filter_by(id=1).first()

    # manha
    hora_inicio = horario1.hora_inicio
    hora_pausa = horario1.hora_pausa
    
    # tarde
    hora_retomada = horario1.hora_retomada
    hora_final = horario1.hora_final

    # manha em minutos
    minutos_inicio = paraMinutos(hora_inicio)
    minutos_pausa = paraMinutos(hora_pausa)

    # tarde em minutos
    minutos_retomada = paraMinutos(hora_retomada)
    minutos_final = paraMinutos(hora_final)

    # tempo de duração de cada atendimento 
    tempo_atendimento = horario1.tempo_atendimento
    minutos_atendimento = paraMinutos(tempo_atendimento)


    # Calcula a diferença entre os minutos
    manhaMinutos = minutos_pausa - minutos_inicio
    tardeMinutos = minutos_final - minutos_retomada

    # quantia de horarios para cada turno
    horarios_manha = manhaMinutos / minutos_atendimento
    horarios_tarde = tardeMinutos / minutos_atendimento
                    #0                    #1                    #2                     #3                #4
    return [int(horarios_manha), int(horarios_tarde), int(minutos_atendimento), int(minutos_inicio), int(minutos_retomada)]

def listaHorarios():
    tempo = 0
    horarios = calculaHorarios()
    lista_horarios = []
    tempo = horarios[3] # tempo que inicia a manha
    tempo2 = horarios[4] # tempo que inicia a tarde
    lista_horarios.append("{}:00".format(int(tempo / 60)))
    for i in range(horarios[0]):
        if i != 0:
            tempo = tempo + horarios[2]
            tempoh = tempo // 60
            tempom = tempo % 60
            tempo_formatado = "{:02}:{:02}".format(tempoh, tempom)
            lista_horarios.append(tempo_formatado)
    
    lista_horarios.append("{}:00".format(int(tempo2 / 60)))

    for i in range(horarios[1]):
        if i != 0:
            tempo2 = tempo2 + horarios[2]
            tempoh = tempo2 // 60
            tempom = tempo2 % 60
            tempo_formatado = "{:02}:{:02}".format(tempoh, tempom)
            lista_horarios.append(tempo_formatado)

    return lista_horarios


