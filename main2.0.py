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
                ram[ram.index(pagina_a_remover)] = pagina_atual

   
    print("Faltas de página:", page_faults)
    return page_faults

def nru(array_list, n_molduras, ciclo_clock):
    ram = []  # Molduras na memória
    page_faults = 0
    bits_R = {}  # Dicionário para armazenar os bits R das páginas
    bits_M = {}  # Dicionário para armazenar os bits M das páginas
    cicloR = {}  # Dicionário para armazenar o último ciclo de acesso de cada página

    for clock in range(len(array_list)):
        pagina_atual = int(array_list[clock][0])  # Página acessada
        tipo_acesso = array_list[clock][2]  # 'R' ou 'W'

        if cicloR:
            for pages in cicloR:
                cicloR[pages] -=1
                if cicloR[pages] == 0:
                    bits_R[pages] = 0

        # Inicializar os bits R e M caso a página seja nova
        if pagina_atual not in bits_R:
            bits_R[pagina_atual] = 0
        if pagina_atual not in bits_M:
            bits_M[pagina_atual] = 0

        # Atualizar os bits R e M com base no tipo de acesso
        bits_R[pagina_atual] = 1
        if tipo_acesso == 'W':
            bits_M[pagina_atual] = 1

        # Verificar se há falta de página
        if pagina_atual not in ram:
            page_faults += 1

            if len(ram) < n_molduras:  # Ainda há espaço na RAM
                ram.append(pagina_atual)
            else:  # Substituir uma página usando NRU
                categorias = {0: [], 1: [], 2: [], 3: []}
                for pagina in ram:
                    if bits_R[pagina] == 1 and bits_M[pagina] == 1:
                        categorias[3].append(pagina)
                    elif bits_R[pagina] == 1 and bits_M[pagina] == 0:
                        categorias[2].append(pagina)
                    elif bits_R[pagina] == 0 and bits_M[pagina] == 1:
                        categorias[1].append(pagina)
                    else:
                        categorias[0].append(pagina)

                # Escolher uma página da menor categoria não vazia
                for prioridade in range(4):
                    if categorias[prioridade]:
                        pagina_a_remover = categorias[prioridade][0]
                        break

                ram[ram.index(pagina_a_remover)] = pagina_atual

        # Atualizar o último ciclo de acesso da página atual
        cicloR[pagina_atual] = ciclo_clock

    print("Faltas de página (NRU):", page_faults)
    return page_faults

def relogio(array_list, n_molduras):
    ram = []  # Molduras na memória
    page_faults = 0
    ponteiro = 0  # Ponteiro circular
    bits_R = {}  # Bits R das páginas

    for clock in array_list:
        pagina_atual = int(clock[0])  # Página acessada

        if ponteiro == len(ram):
            ponteiro = 0

        # Atualizar bit R da página atual
        if pagina_atual not in bits_R:
            bits_R[pagina_atual] = 0
        bits_R[pagina_atual] = 1

        # Verificar se a página já está na RAM
        if pagina_atual not in ram:
            page_faults += 1

            if len(ram) < n_molduras:  # Ainda há espaço na RAM
                ram.append(pagina_atual)
            else:  # Substituir uma página usando ponteiro circular
                while True:
                    pagina_candidata = ram[ponteiro]
                    if bits_R[pagina_candidata] == 0:  # Página não referenciada recentemente
                        ram[ponteiro] = pagina_atual
                        break
                    else:  # Página foi referenciada recentemente; redefinir bit R e avançar ponteiro
                        bits_R[pagina_candidata] = 0  # Ajustar o ponteiro circular

            # Atualizar o ponteiro circular após substituição
            ponteiro += 1

    print("Faltas de página (Relógio):", page_faults)
    return page_faults


def wsclock(referencias, n_molduras, ciclo_relogio):
    ram = []  # Molduras na memória (buffer circular)
    page_faults = 0
    ponteiro = 0  # Ponteiro do relógio
    timestamps = {}  # Último ciclo de acesso de cada página
    bits_R = {}  # Bits de Referência

    for ref in referencias:
        # Extrair os valores da referência
        pagina_atual = int(ref[0])  # Número da página
        t_atual = int(ref[1])       # Tempo de acesso
        operacao = ref[2]           # Operação (R ou W)

        # Atualizar bit R e timestamp
        if pagina_atual not in bits_R:
            bits_R[pagina_atual] = 0  # Página nova assume R=0 inicialmente
            timestamps[pagina_atual] = t_atual  # Define o tempo de acesso

        bits_R[pagina_atual] = 1  # Sempre marca a página como usada
        timestamps[pagina_atual] = t_atual  # Atualiza o tempo de acesso

        # Se a página já está na RAM, não há falta de página
        if pagina_atual in ram:
            continue

        # Caso contrário, ocorre uma falta de página
        page_faults += 1

        if len(ram) < n_molduras:
            ram.append(pagina_atual)  # Ainda há espaço na RAM
        else:
            inicio = ponteiro  # Salva a posição inicial do ponteiro
            substituida = False

            while True:
                pagina_candidata = ram[ponteiro]
                idade_pagina = t_atual - timestamps[pagina_candidata]  # Tempo desde o último uso

                # Verifica se o bit R foi resetado após 'ciclo_relogio' ciclos
                if t_atual - timestamps[pagina_candidata] >= ciclo_relogio:
                    bits_R[pagina_candidata] = 0

                if bits_R[pagina_candidata] == 0 and idade_pagina > 6:
                    # Página pode ser substituída
                    ram[ponteiro] = pagina_atual
                    timestamps[pagina_atual] = t_atual
                    bits_R[pagina_atual] = 1  # Nova página é marcada como referenciada
                    substituida = True
                    break
                else:
                    bits_R[pagina_candidata] = 0  # Resetar bit R
                    ponteiro = (ponteiro + 1) % n_molduras  # Avançar ponteiro

                    if ponteiro == inicio:  # Se rodou toda a RAM e não achou, substituir qualquer página
                        ram[ponteiro] = pagina_atual
                        timestamps[pagina_atual] = t_atual
                        bits_R[pagina_atual] = 1  # Nova página é marcada como referenciada
                        substituida = True
                        break

            if not substituida:
                ram[ponteiro] = pagina_atual
                timestamps[pagina_atual] = t_atual
                bits_R[pagina_atual] = 1  # Nova página é marcada como referenciada

    print("Faltas de página (WSClock):", page_faults)
    return page_faults


def process_memory(array_list):
    n_paginas = int(array_list[0][0])
    n_molduras = int(array_list[1][0])
    time_R = int(array_list[2][0])
    del array_list[0:3]
    array_all = []
    array_all.append(otimo(array_list, n_molduras))
    array_all.append(nru(array_list, n_molduras, time_R))
    array_all.append(relogio(array_list, n_molduras))
    array_all.append(wsclock(array_list, n_molduras, time_R))
    return array_all


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
        #Colocar instruções no txt de resultado
        for line in process_memory(array_list):
             write_file.write(str(line) + '\n')


#Mude a quantidade de arquivos
n_arquivos = 3
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
