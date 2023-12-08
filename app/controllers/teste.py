def calculaHorarios():
    return [16, 2, 30, 420, 780]

def listaHorarios():
    tempo = 0
    horarios = calculaHorarios()
    lista_horarios = []
    tempo = horarios[3]
    lista_horarios.append("{}:00".format(int(tempo / 60)))
    for i in range(horarios[0]):
        if i != 0:
            tempo = tempo + horarios[2]
            tempoh = tempo // 60
            tempom = tempo % 60
            tempo_formatado = "{:02}:{:02}".format(tempoh, tempom)
            lista_horarios.append(tempo_formatado)
    
    return lista_horarios


print(listaHorarios())