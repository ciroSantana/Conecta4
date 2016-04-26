# coding=utf-8
import games
import random


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

            if (c_index[0] == f_index == 0): self.modo_facil(state)

            if (c_index[0] > f_index[0]):
                return c_index[1]
            else:
                return f_index[1]

    def tratar_columnas(self, state):

        c_ocup = self.cuenta_piezas_columna(state)     #contar numero de piezas por columna
        contiguos = self.contiguos_validos_columnas(state, c_ocup)  #contar número de contiguos válidos

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

    def contiguos_validos_columnas(self, state, c_ocup):    #devuelve vector[] con (fin,count)

        contiguos = []

        for x in range(1,8): #recorrer columnas
            count = 0
            contiguos.append([])
            if (c_ocup[x-1] in (0,6)):    #si la columna está vacía o llena, parar
                continue

            item = state.board.get((x,1))       #si la columna tiene elementos, coger el primero

            for y in range(1,7):
                item2 = state.board.get((x,y))
                if (item == state.board.get((x,y))):  #contar el número de elementos contiguos iguales
                    count+=1

                else:
                    contiguos[x-1].append((y-1, count))

                    if (count == c_ocup[x-1]): break

                    count = 1
                    item = state.board.get((x,y))

        #descartes
        for x in range(0,len(contiguos)):
            y = len(contiguos[x])-1
            while (y > -1):
                if (4-contiguos[x][y][1] + c_ocup[x]) > 6:  #si no se puede hacer 4 en raya en esa columna
                    for z in range(len(contiguos[x])-1,-1,-1):  #borramos todas las ocurrencias de la columna
                        contiguos[x].__delitem__(z)
                    break
                if (state.board.get((x+1,contiguos[x][y][0] +1), '.') != '.'):   #si está bloqueada
                    contiguos[x].__delitem__(y)
                y-=1
        return contiguos

    def maximo(self, state=None, contiguos=[], fila=False):       #devuelve el par (columna_tomove, conectados)
        linea, count = 0, 0

        for x in range(0,len(contiguos)):
            for y in range(0,len(contiguos[x])):
                if (contiguos[x][y][1] > count):
                    count = contiguos[x][y][1]

        if (fila) and (len(contiguos[linea]) != 0):
            linea = self.columna_tomove(state, linea, contiguos[linea][0][0], contiguos[linea][0][1])

        return (linea,count)

    def tratar_filas(self, state):  #diferencia con columnas: después de saber qué fila es la mayor, hay que decir la columna a la que mover

        f_ocup = self.cuenta_piezas_fila(state)#contar numero de piezas por fila
        contiguos = self.contiguos_validos_filas(state, f_ocup)

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

    def contiguos_validos_filas(self, state, f_ocup):

        contiguos = []
        #recorrer filas
        for y in range(1,7):
            contiguos.append([])
            count = 0
            if (f_ocup[y-1] in (0,7)):    #si la fila está vacía o llena, siguiente
                continue


            item = state.board.get((1,y)) #si la fila tiene elementos, coger el primero
            for x in range(1,8):
                if state.board.get((x,y)) == item:    #contar el número de elementos contiguos iguales
                    count+=1

                else:
                    contiguos[y-1].append((x-1,count))   # x = fin

                    if (count == f_ocup[y-1]): break

                    count = 1
                    item = state.board.get((x,y))

        #descartes
        for x in range(0,len(contiguos)):
            y = len(contiguos[x])-1
            while (y > -1):
                if (4-contiguos[x][y][1] + f_ocup[x]) > 7:  #si no se puede hacer 4 en raya en esa fila
                    for z in range(len(contiguos[x])-1,-1,-1):  #borramos todas las ocurrencias de la fila
                        contiguos[x].__delitem__(z)
                    break
                if (self.busca_bloqueos(state, x+1, contiguos[x][y][0], contiguos[x][y][1])):   #si está bloqueada
                    contiguos[x].__delitem__(y)
                y-=1

        return contiguos

    def busca_bloqueos(self, state, fila, fin, count):  #devuelve true si no se puede hacer 4 en raya en esa fila

        ini = fin - (count-1)   #ultima pieza por la izda

        aux = 0
        for x in range(ini, 0, -1):    #busca por la izda
            if (state.board.get((x,fila), '.') == '.'):
                aux+=1
            else:
                if (aux + count >= 4):
                    return 0

        aux = 0
        for x in range(fin+1, 8):       #busca por la dcha
            if (state.board.get((x,fila),'.') == '.'):
                aux+=1

            else:
                if (aux + count >= 4):
                    return 0

        return 1

    def columna_tomove(self, state, fila_tomove, fin, count):

        i = 0
        ini = fin - count
        for x in range(ini,0, -1):
            if (state.board.get((x, fila_tomove), '.') == '.'):
                i+=1
            else:
                break

        d = 0
        for x in range(fin+1,8):
            if (state.board.get((x, fila_tomove), '.') == '.'):
                d+=1
            else:
                break

        if (i>d):
            return ini + i
        else:
            return fin + d

    #####################################################333
    def modo_medio(self, state):    #que se mueva a la columna que más ocupada esté

        dict = self.busqueda_horizontal(state)
        dict.update(self.busqueda_vertical(state))
        return max(dict, key=dict.get)

    def busqueda_horizontal(self, state):

        suma_fila_max = [0,0]

        for y in range(6, 0, -1):       #recorre en altura
            count = 0
            item = state.board.get((1,y))
            for x in range(1, 7+1):     #recorre en anchura
                 if (state.board.get((x, y)) == item):
                     count+=1

                 else:
                     if (count > suma_fila_max[1]):
                         suma_fila_max = [y,count]
                     count = 0
                     item = state.board.get((x, y))

            if  count > suma_fila_max[1]:
                suma_fila_max = [y, count]

        return {self.mejor_columna(state, suma_fila_max[0]):suma_fila_max[1]}

    def mejor_columna(self, state, fila):
        d = {}
        item = state.board.get((1,fila))
        maximo = [0,1]
        pos = 0

        for x in range(2, 5):     #recorre en anchura por la izda
             count = 0
             if (state.board.get((x, fila)) == item):
                 count+=1
             else:

                 if (count > maximo[1]):
                     maximo[pos,count]
                 pos = x
                 izquierda = {x:count}
                 item = state.board.get((x, fila))


        item = state.board.get((7,fila))
        pos = 7
        for x in range(6, 3, -1):     #recorre en anchura por la dcha
             count = 0
             if (state.board.get((x, fila)) == item):
                 count+=1
             else:
                 if (count > maximo[1]):
                     maximo[pos, count]
                 pos = x
                 derecha = {x:count}
                 item = state.board.get((x, fila))

        return maximo[0]

    def busqueda_vertical(self, state):

        suma_columna_max = [0,0]

        for x in range(1, 7+1):     #recorre en anchura
            count = 0
            item = state.board.get((x,1))
            for y in range(6, 0, -1):      #recorre en altura
                if ((state.board.get(x,y)) == item):
                    count+= 1

                else:
                    if (count > suma_columna_max[1]):
                         suma_fila_max = [x,count]
                    item = state.board.get(x,y)
                    count = 0

            if count > suma_columna_max[1]:
                suma_columna_max = [x, count]

        return {suma_columna_max[0]:suma_columna_max[1]}
################################################################
    def display_heuristicas(self):
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

    def get_modoText(self, i):  # cambiar por dispplay_modes si no se va a usar el muestreo individual
        return self.modos[i]

    def get_modoFunction(self, i):
        return self.modos_functions[i]

    def get_auxHeur(self, i):
        return self.auxHeur[i]

    def get_auxHeur_length(self):
        return len(self.auxHeur)

    def get_heurFunction(self, index):
        return self.auxHeur_functions[index]