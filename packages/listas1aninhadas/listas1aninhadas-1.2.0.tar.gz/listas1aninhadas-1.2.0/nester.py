"""Este é o modulo listas1aninhadas.py, e fornece uma funcão chamada print_lol() que imprime listas que podem ter
 ou não listas aninhadas"""
def print_lol(the_list, level=0):
    """ Esta função requer um argumento posicionalchamado 'the_list, que é qualquer lista python(de possiveis listas
aninhadas).
Foi inserido um segundo argumento(level) que define a tabulação de cada lista"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1)
        else:
            for tab_stop in range(level):
                print("\t", end=" ")
            print(each_item)