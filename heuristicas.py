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

            return c_index + f_index

    def tratar_columnas(self, state):

        c_ocup = self.cuenta_piezas_columna(state)     #contar numero de piezas por columna
        contiguos = self.contiguos_columnas(state, c_ocup)  #contar número de contiguos válidos

        return self.maximo(contiguos) #

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

            item = state.board.get((x,1))       #si la columna tiene elementos, coger el primero
            for y in range(1,8):
                if (item == state.board.get((x,y))):  #contar el número de elementos contiguos iguales
                    count+=1

                else:
                    if (item in ('X', 'O')):
                        contiguos[x-1].append((count, item))

                    if (count == c_ocup[y-1]): break

                    count = 1
                    item = state.board.get((x,y))

        return contiguos

    def maximo(self, contiguos):       #devuelve el par (columna_tomove, conectados)
        count = 0

        for x in range(0,len(contiguos)):
            for y in range(0,len(contiguos[x])):
                if contiguos[x][y][1] == 'X': count += (5^contiguos[x][y][0])
                else: count += (5^contiguos[x][y][0]) * -1

        return count

    def tratar_filas(self, state):  #diferencia con columnas: después de saber qué fila es la mayor, hay que decir la columna a la que mover

        f_ocup = self.cuenta_piezas_fila(state)#contar numero de piezas por fila
        contiguos = self.contiguos_filas(state, f_ocup)

        return self.maximo(contiguos) #buscar fila max, columna max, y devuelve (col_max,count)

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
                        contiguos[y-1].append((count,item))   # x = fin

                    if (count == f_ocup[y-1]): break

                    count = 1
                    item = state.board.get((x,y))


        return contiguos

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