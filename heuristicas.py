# coding=utf-8
import random

class Heuristicas:

    def memoize(f):

        memo = {}

        def helper(self,x):
            estado = frozenset(x.board.items())

            if estado not in memo:
                memo[estado] = f(self,x)

            return memo[estado]

        return helper

    def __init__(self, nombre):
        self.text_modos = ["Modo aleatorio", "Modo facil", "Modo medio", "Modo dificil"]
        self.funct_modos = [(self.modo_random,2), (self.mi_heuristica,2), (self.mi_heuristica,4), (self.mi_heuristica,6)]

        self.nombre = nombre
        index = self.decide_modo()

        self.modo = self.funct_modos[index][0]
        self.depth = self.funct_modos[index][1]

    def modo_random(self, state):
        return random.randint(-100, 100)

    @memoize
    def mi_heuristica(self, state):

        columnas = self.contiguos_columnas(state)  #tratar columna

        filas = self.contiguos_filas(state) #tratar fila

        return self.maximo(filas, factor=1000) + self.maximo(columnas, factor=1000)

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

    def contiguos_columnas(self, state):    #devuelve vector[] con (fin,count)

        contiguos = []
        c_ocup = self.cuenta_piezas_columna(state)

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

    def maximo(self, contiguos, factor):       #devuelve el par (columna_tomove, conectados)
        count = 0

        for x in range(0,len(contiguos)):
            for y in range(0,len(contiguos[x])):
                if contiguos[x][y][1] == 'X': count += (factor**contiguos[x][y][0])
                else: count += (factor**contiguos[x][y][0])*(-1)

        return count

    def cuenta_piezas_fila(self, state):

        f = []
        for y in range(1,7):
            count = 0
            for x in range(1,8):
                if (state.board.get((x,y),'.') != '.'): #contar numero de apariciones indistintamente del tipo
                    count += 1

            f.append(count)  #rellenar en un vector

        return f

    def contiguos_filas(self, state):

        contiguos = []
        f_ocup = self.cuenta_piezas_fila(state)
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

    def decide_modo(self):      #método para heuristicas de otros compañeros
        print "******************************"
        print "Definir modo de juego de " + self.nombre + ": "

        i = 0
        for h in self.text_modos:
            print "(" + str(i + 1) + ")" + h
            i += 1

        index = int(str(raw_input("Numero de modo deseado: ")).strip())-1
        print "Ha elegido: " + self.text_modos[index] + "."
        print "******************************"

        return index