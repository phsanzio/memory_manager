def otimo(array_list, n_molduras):
    ram = []  # Lista para representar as molduras na memória
    page_faults = 0  # Contador de faltas de página

    # Iterar sobre cada acesso no array_list
    for i in range(len(array_list)):
        pagina_atual = int(array_list[i][0])  # Página atual sendo acessada

        # Verificar se a página já está na RAM
        if pagina_atual not in ram:
            page_faults += 1  # Incrementar as faltas de página

            if len(ram) < n_molduras:  # Há espaço na RAM
                ram.append(pagina_atual)
            else:  # Substituir uma página
                # Encontrar a página que será usada mais tarde ou nunca mais
                paginas_futuras = [int(array_list[j][0]) for j in range(i + 1, len(array_list))]
                indices_futuros = []

                for pagina in ram:
                    if pagina in paginas_futuras:
                        indices_futuros.append(paginas_futuras.index(pagina))
                    else:
                        indices_futuros.append(float('inf'))  # Página nunca mais será usada

                # Substituir a página com maior índice futuro (ou nunca usada)
                pagina_a_remover = ram[indices_futuros.index(max(indices_futuros))]
                ram.remove(pagina_a_remover)
                ram.append(pagina_atual)

    print("RAM final:", ram)
    print("Faltas de página:", page_faults)
    return page_faults
    
def process_memory(array_list):
    n_paginas = int(array_list[0][0])
    n_molduras = int(array_list[1][0])
    time_R = int(array_list[2][0])
    del array_list[0:3]
    otimo(array_list, n_molduras)
    # fifo_result = fifo(array_list)
    # sjf_result = sjf(array_list)
    # srt_result = srt(array_list)
    # rr_result = rr(array_list, quantum)
    # array_all = []
    # array_all.append(fifo_result)
    # array_all.append(sjf_result)
    # array_all.append(srt_result)
    # array_all.append(rr_result)
    # return array_all



def text_generator(read_file, write_file):
    with open(read_file, 'r') as read_file, open(write_file, 'w') as write_file:
        #Colocar instruções no array_list
        array_list = []
        for line in read_file:
            array_temp = []
            if line != '':
                for element in line.split():
                    array_temp.append(element)
                array_list.append(array_temp)
        process_memory(array_list)
        #Colocar instruções no txt de resultado
        # for line in process_memory(array_list):
        #     write_file.write(line + '\n')


#Mude a quantidade de arquivos
n_arquivos = 1
#Coloque o caminho exato do arquivo, ex: pc/documentos/testes/
caminho_arquivo = ""
for i in range(0, n_arquivos):
    username = 'Pedro Sanzio e Lucas Martins'
    if i + 1 < 10:
        read_file = f'{caminho_arquivo}TESTE-0{i+1}.txt'
    else:
        read_file = f'{caminho_arquivo}TESTE-{i+1}.txt'
    filename = read_file.replace('.txt', '-RESULTADO')
    write_file = str(filename) + '.txt'
    text_generator(read_file, write_file)