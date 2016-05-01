# coding=utf-8
import games
import random
import math


class Heuristicas:

    def __init__(self):
        self.modos = ["Modo facil", "Modo medio", "Modo_dificil"]
        self.modos_functions = [self.modo_facil, self.modo_medio, self.modo_dificil]
        self.auxHeur = []
        self.auxHeur_functions = []

    def modo_facil(self, state):
        return random.randint(-100, 100)

    def modo_dificil(self, state):

            c_index = self.tratar_columnas(state)  #tratar columna

            f_index = self.tratar_filas(state) #tratar fila

            if (c_index[1] > f_index[1]):       #heuristica = max_piezas_contiguas*jugador
                return math.sqrt(c_index[1])*c_index[2]

            else:
                return math.sqrt(f_index[1])*f_index[2]

    def tratar_columnas(self, state):

        c_ocup = self.cuenta_piezas_columna(state)     #contar numero de piezas por columna
        contiguos = self.contiguos_columnas(state, c_ocup)  #contar número de contiguos válidos

        return self.maximo(contiguos=contiguos) #la columna con mayor numero de apariciones contiguas, no invalidas, sera la mejor

    def cuenta_piezas_columna(self, state):     #devuelve v donde v[i] = nº piezas en columna i

        c = []
        for x in range(1,8):    #recorrer columnas
            count = 0
            for y in range(1,7):
                #contar numero de apariciones indistintamente del tipo
                if (state.board.get((x,y), '.') != '.'):
                    count += 1
            #rellenar en un vector
            c.append(count)

        #devolver vector
        return c

    def contiguos_columnas(self, state, c_ocup):    #devuelve vector[] con (fin,count)

        contiguos = []

        for x in range(1,8): #recorrer columnas
            count = 0
            contiguos.append([])
            if c_ocup[x-1] == 0:    #si la columna está vacía, parar
                continue

            item = state.board.get((x,c_ocup[x-1]))       #si la columna tiene elementos, coger el primero
            for y in range(c_ocup[x-1],-1,-1):
                if (item == state.board.get((x,y))):  #contar el número de elementos contiguos iguales
                    count+=1

                else:
                    contiguos[x-1].append((y+1, count, item))
                    break
        #descartes
        for x in range(0,len(contiguos)):
            y = len(contiguos[x])-1
            while (y > -1):

                if (contiguos[x][y][1] >= 4):               #si ya hay 4 en raya, continua descartando
                    y-=1
                    continue
                if (4-contiguos[x][y][1] + c_ocup[x]) > 6:  #si no se puede hacer 4 en raya en esa columna
                    for z in range(len(contiguos[x])-1,-1,-1):  #borramos todas las ocurrencias de la columna
                        contiguos[x].__delitem__(z)
                    break
                if (state.board.get((x+1,contiguos[x][y][0] +1), '.') != '.'):   #si está bloqueada
                    contiguos[x].__delitem__(y)
                y-=1
        return contiguos

    def maximo(self, state=None, contiguos=[], fila=False):       #devuelve el par (columna_tomove, conectados)
        linea, count, jugador = 0, 0, 0

        for x in range(0,len(contiguos)):
            for y in range(0,len(contiguos[x])):
                if (contiguos[x][y][1] > count):
                    count = contiguos[x][y][1]
                    linea = x+1
                    if (contiguos[x][y][1] == 'O'): jugador = -1
                    else: jugador = 1


        if (fila) and (len(contiguos[linea-1]) != 0):
            linea = self.columna_tomove(state, linea, contiguos[linea-1][0][0], contiguos[linea-1][0][1])

        return (linea,count,jugador)

    def tratar_filas(self, state):  #diferencia con columnas: después de saber qué fila es la mayor, hay que decir la columna a la que mover

        f_ocup = self.cuenta_piezas_fila(state)#contar numero de piezas por fila
        contiguos = self.contiguos_filas(state, f_ocup)

        return self.maximo(state, contiguos, fila=1) #buscar fila max, columna max, y devuelve (col_max,count)

    def cuenta_piezas_fila(self, state):

        f = []
        for y in range(1,7):
            count = 0
            for x in range(1,8):
                if (state.board.get((x,y),'.') != '.'): #contar numero de apariciones indistintamente del tipo
                    count += 1

            f.append(count)  #rellenar en un vector

        return f

    def contiguos_filas(self, state, f_ocup):

        contiguos = []
        #recorrer filas
        for y in range(1,7):
            contiguos.append([])
            count = 0
            if f_ocup[y-1] == 0:    #si la fila está vacía, siguiente
                continue

            item = state.board.get((1,y)) #si la fila tiene elementos, coger el primero
            for x in range(1,9):    #LO HE CAMBIADO DE 8 A 9 PARA QUE CUENTE CON LA ÚLTIMA COLUMNA DE LA FILA
                if state.board.get((x,y)) == item:    #contar el número de elementos contiguos iguales
                    count+=1

                else:

                    if (item in ('X','O')):
                        contiguos[y-1].append((x-1,count,item))   # x = fin

                    if (count == f_ocup[y-1]): break    #si ya se ha acabado de comprobar toda la fila  #no está haciendo nada: en caso de que los elementos
                                                        # estén separados, count va tomando valores cero, y su suma es mayor que el f_ocup, pero no interrumpe

                    count = 1
                    item = state.board.get((x,y))

        #descartes
        for x in range(0,len(contiguos)):
            y = len(contiguos[x])-1
            while (y > -1):

                if (contiguos[x][y][1] >= 4):       #si ya hay 4 en raya en la fila, seguir descartando
                    y-=1
                    continue

                if (4-contiguos[x][y][1] + f_ocup[x]) > 7:  #si no se puede hacer 4 en raya en esa fila
                    for z in range(len(contiguos[x])-1,-1,-1):  #borramos todas las ocurrencias de la fila
                        contiguos[x].__delitem__(z)
                    break
                if (self.busca_bloqueos(state, x+1, contiguos[x][y][0], contiguos[x][y][1])):   #si está bloqueada
                    contiguos[x].__delitem__(y)
                y-=1

        return contiguos

    def busca_bloqueos(self, state, fila, fin, count):  #devuelve true si no se puede hacer 4 en raya en esa fila

        ini = fin - (count-1)   #primera pieza por la izda

        aux = 0
        for x in range(ini-1, 0, -1):    #busca por la izda

            if (state.board.get((x,fila), '.') == '.'):
                aux+=1

            if (aux + count >= 4):
                return 0

        aux = 0
        for x in range(fin+1, 8):       #busca por la dcha

            if (state.board.get((x,fila),'.') == '.'):
                aux+=1

            if (aux + count >= 4):
                return 0

        return 1

    def columna_tomove(self, state, fila_tomove, fin, count):   #devuelve la columna a la que moverse dentro de la fila
                                                                #según los espacios libres

        izq = 0
        ini = fin - count
        for x in range(ini,0, -1):
            if (state.board.get((x, fila_tomove), '.') == '.'):
                izq+=1
            else:
                break

        dcha = 0
        for x in range(fin+1,8):
            if (state.board.get((x, fila_tomove), '.') == '.'):
                dcha+=1
            else:
                break

        if (izq>dcha):
            return ini
        else:
            return fin + 1


    def modo_medio(self, state):
        return "No está implementado"

    def display_heuristicas(self):      #método para heuristicas de otros compañeros
        print "Heuristicas disponibles"

        i = 0
        for h in self.auxHeur:
            print "(" + i + 1 + ")" + h
            i += 1

    def display_modos(self):
        print "Modos disponibles"

        i = 0
        for h in self.modos:
            print "(" + str(i+1) + ")" + h
            i += 1

    def get_modoText(self, i):  # cambiar por display_modes si no se va a usar el muestreo individual
        return self.modos[i]

    def get_modoFunction(self, i):
        return self.modos_functions[i]

    def get_auxHeur(self, i):
        return self.auxHeur[i]

    def get_auxHeur_length(self):
        return len(self.auxHeur)

    def get_heurFunction(self, index):
        return self.auxHeur_functions[index]