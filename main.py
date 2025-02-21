def otimo(array_list, n_molduras):
    clock = 0
    ram = []
    memory_dict = {}
    page_faults = 0
    for i in range(len(array_list)):
        memory_dict[i] = {'page': int(array_list[i][0]), 'acess': int(array_list[i][1]), 'type': array_list[i][2], 'bit_R': 0, 'bit_M': 0}
    for pages in memory_dict:
        if memory_dict[pages]['acess'] == clock:
            if pages not in ram:
                page_faults += 1
                if len(ram) < n_molduras:
                    ram.append(memory_dict[pages])
                else:
                    clock_max = {}
                    for pages_left in memory_dict[pages:]:
                        for pages_ram in ram:
                            if memory_dict[pages_left]['page'] == ram[pages_ram]['page']:
                                clock_max.setdefault(pages_ram, ram[pages_ram]['page'], memory_dict[pages_left]['acess'])
                            print (clock_max)

            
                    

        clock += 1
    print(ram)
    print(page_faults)

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