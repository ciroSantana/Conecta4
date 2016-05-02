import games
import heuristicas

def decide_turno():
    return str(raw_input("Decida si empieza jugando maquina (X) o jugador (O): ")).strip().upper()

def decide_modo(h):
    h.display_modos()
    index = int(str(raw_input("Numero de modo deseado: ")).strip())-1
    print "Ha elegido " + h.get_modoText(index) + "."
    return h.get_modoFunction(index)

def decide_jugador():
    return str(raw_input("Jugar con heuristica: si (V) no (X): ")).strip().upper()

def decide_heuristica(h):

    for i in range(0, h.get_auxHeur_length()):
        print "(" + str(i+1) + ")" + h.get_auxHeur(i)

    index = int(str(raw_input("Numero de heuristica deseada: ")).strip())-1
    print "Ha elegido " + h.get_auxHeur(index)
    return h.get_heurFunction(index)

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

            move = games.alphabeta_search(state, game, eval_fn=heur_modo)

            state = game.make_move(move, state)
            player = 'O'
        print "-------------------"
        if game.terminal_test(state):
            game.display(state)
            print "Final de la partida"
            break


#game = games.TicTacToe(h=3,v=3,k=3)


player = decide_turno()
game = games.ConnectFour(player=player)
state = game.initial
h = heuristicas.Heuristicas()
funcion_modo = decide_modo(h)
maquina2 = decide_jugador()

if (maquina2 == 'V'):
    maq_maq(game, state, player, funcion_modo, decide_heuristica(h))

else:
    maq_jug(game, state, player, funcion_modo)







