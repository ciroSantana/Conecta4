import random

class Heuristicas:

    def __init__(self, nombre):
        self.text_modos = ["Modo aleatorio", "Modo facil", "Modo medio", "Modo dificil"]
        self.funct_modos = [(self.modo_random,0), (self.mi_heuristica,2), (self.mi_heuristica,4), (self.mi_heuristica,6)]

        if (nombre == 'O'): self.comodin = -1
        else: self.comodin = 1

        self.nombre = nombre
        index = self.decide_modo()

        self.modo = self.funct_modos[index][0]
        self.depth = self.funct_modos[index][1]



    #Muestra modos de dificultad y selecciona
    def decide_modo(self):
        print "******************************"
        print "Definir modo de juego de jugador " + self.nombre + ": "

        i = 0
        for h in self.text_modos:
            print "(" + str(i + 1) + ")" + h
            i += 1

        index = int(str(raw_input("Numero de modo deseado: ")).strip())-1
        print "Ha elegido: " + self.text_modos[index] + "."
        print "******************************"

        return index

    def memoize(f):

        memo = {}

        def helper(self, state):
            estado = frozenset(state.board.items())

            if estado not in memo:
                memo[estado] = f(self, state)

            return memo[estado]

        return helper

    def modo_random(self, state):
        return random.randint(-100, 100)


    @memoize
    #Calcula suma heuristica por filas, columnas y diagonales
    def mi_heuristica(self, state):

        pos = [1,1]

        suma = self.trata_filas(state.board, pos, state.to_move)
        suma += self.trata_columnas(state.board, pos, state.to_move)
        suma += self.trata_diagonales(6, state.board, pos, state.to_move, -1) #descendente
        suma += self.trata_diagonales(1, state.board, pos, state.to_move, 1)   #ascendente

        return suma

    #recorrido en columnas
    def trata_columnas(self, tablero, pos, jugador):
        valor = 0
        for y in range(6):
            while pos[0] <= 7:
                pos, aux = self.suma(tablero, pos, jugador, 1, 0)
                valor += aux
                pos[0] += 1

            pos[0] = 1
            pos[1] += 1

        return valor

    #recorrido en filas
    def trata_filas(self, tablero, pos, jugador):
        valor = 0
        for x in range(7):
            while pos[1] <= 6:
                pos, aux = self.suma(tablero, pos, jugador, 0, 1)
                valor += aux
                pos[1] += 1

            pos[0] += 1
            pos[1] = 1

        return valor

    #recorrido diagonal
    #dx: (1) ascendente, (-1) descendente
    def trata_diagonales(self, ini, tablero, pos, jugador, dx):
        valor = 0
        sentido_ini = 0
        for i in range(2):
            for j in range(2, 8):
                while pos[1] <= 6:
                    #suma de la diagonal y recoge posicion final para
                    pos, aux = self.suma(tablero, pos, jugador, dx, 1)
                    valor += aux
                    #seguir recorriendo a partir de la posicion anterior
                    pos[0] += dx
                    pos[1] += 1

                if sentido_ini:
                    pos[0], pos[1] = ini, j
                else:
                    pos[0], pos[1] = j, 1

            sentido_ini = not sentido_ini

        if (valor >= 1500): valor -= 1000
        if (valor <= -1500): valor += 1000

        return valor

    #Devuelve la suma de valor de la linea y posicion final
    #Recorre en sentido_ini (dx,dy)
    def suma(self, board, pos, player, dx, dy):
        suma = 0
        while tuple(pos) in board:
            pos, aux = self.mi_kinrow(board, pos, player, (dx, dy))
            suma += aux

            if (player == 'X'):
                pos, aux = self.mi_kinrow(board, pos, 'O', (dx, dy))
            else:
                pos, aux = self.mi_kinrow(board, pos, 'X', (dx, dy))

            suma += aux

        return pos, suma*self.comodin   #comodin en caso de heuristica jugador O

    #Devuelve el valor de las fichas adyacentes de player y la ultima pos
    #Recorre a partir de (x, y) en sentido (dx, dy)
    #(dx, dy) --> (0,1) columnas, (1,0) filas, (1,1) diagonales
    def mi_kinrow(self, board, (x, y), player, (dx, dy)):

        contiguos = 0  # n is number of moves in row
        while board.get((x, y)) == player:
            contiguos += 1
            x, y = x + dx, y + dy

        if (player == 'X'):
            value = self.get_value(contiguos)
        else:
            value = -self.get_value(contiguos)

        return [x, y], value

    def get_value(self, contiguos):
        if contiguos >= 4:
            return 15000
        elif contiguos == 3:
            return 5000
        elif contiguos == 2:
            return 1000
        else:
            return 0


    #el modo maquina no funciona bien porque le asigna valores negativos al usuario
    #con el simbolo O, luego siempre va a ser negativo, y no escoge la heuristica de "mejor" valor