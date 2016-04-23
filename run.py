import games
import heuristicas

def decide_turno():
    return str(raw_input("Empieza jugando maquina (X) o jugador (O): ")).strip().upper()

def decide_modo():
    i = 1
    print "Niveles de juego de la maquina: "
    while (i < 4):
        print "(" + str(i) + ")" + heuristicas.get_modo(i)
        i+=1

    index = int(str(raw_input("Numero de heuristica deseada: ")).strip())-1
    print "Ha elegido " + heuristicas.get_modo(index) + "."
    return index

def decide_jugador():
    return str(raw_input("Jugar con heuristica: si (V) no (X): ")).strip().upper()

def decide_heuristica():

    size = heuristicas.get_auxHeur_length()
    i = 1
    while (i < size+1):
        print "(" + str(i) + ")" + heuristicas.get_auxHeur(i)
        i+=1

    return int(str(raw_input("Numero de heuristica deseada: ")).strip())-1

def maq_maq(game, state, player, heur_modo, heur2):
    while True:
        print "Jugador a mover:", game.to_move(state)
        game.display(state)

        if player == 'O':
            print "Thinking maquina B..."
            move = games.alphabeta_search(state, game, heur2)
            state = game.make_move(move, state)
            player = 'X'
        else:
            print "Thinking maquina A..."
            #move = games.minimax_decision(state, game)
            #move = games.alphabeta_full_search(state, game)

            move = games.alphabeta_search(state, game, heur_modo)

            state = game.make_move(move, state)
            player = 'O'
        print "-------------------"
        if game.terminal_test(state):
            game.display(state)
            print "Final de la partida"
            break

def maq_jug(game, state, player, heur_modo):
    while True:
        print "Jugador a mover:", game.to_move(state)
        game.display(state)

        if player == 'O':
            col_str = raw_input("Movimiento: ")
            coor = int(str(col_str).strip())
            x = coor
            y = -1
            legal_moves = game.legal_moves(state)
            for lm in legal_moves:
                if lm[0] == x:
                    y = lm[1]

            state = game.make_move((x, y), state)
            player = 'X'
        else:
            print "Thinking..."
            #move = games.minimax_decision(state, game)
            #move = games.alphabeta_full_search(state, game)



            move = games.alphabeta_search(state, game, heur_modo)



            state = game.make_move(move, state)
            player = 'O'
        print "-------------------"
        if game.terminal_test(state):
            game.display(state)
            print "Final de la partida"
            break


#game = games.TicTacToe(h=3,v=3,k=3)
game = games.ConnectFour()

state = game.initial

player = decide_turno()
modo = decide_modo()-1
string_modo = "heuristicas." + heuristicas.get_modo(modo) + "()"
maquina2 = decide_jugador()

if (maquina2 == 'V'):
    heuristicas.display_heuristicas()
    heur_index = decide_heuristica()
    string_heur2 = "heuristicas." + heuristicas.get_auxHeur(heur_index) + "()"
    maq_maq(game, state, player, string_modo, heur_index)

else:
    maq_jug(game, state, player, string_modo)







