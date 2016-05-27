import games
import heuristicas

def decide_inicio():
    return str(raw_input("Decida si empieza jugando maquina (X) o jugador (O): ")).strip().upper()
def decide_jugador2():
    return str(raw_input("Modo Automatico si / no: ")).strip().upper()

def maq_maq(game, state, player, heur_maq, heur_jugador2):
    while True:
        print "Jugador a mover:", game.to_move(state)
        game.display(state)

        if player == 'O':
            print "Thinking maquina O..."
            move = games.alphabeta_search(state, game, d=heur_jugador2.depth, eval_fn=heur_jugador2.modo)
            state = game.make_move(move, state)
            player = 'X'
        else:
            print "Thinking maquina X..."

            move = games.alphabeta_search(state, game, d=heur_maq.depth, eval_fn=heur_maq.modo)

            state = game.make_move(move, state)
            player = 'O'
        print "-------------------"
        if game.terminal_test(state):
            game.display(state)
            print "Final de la partida"
            break

def maq_jug(game, state, player, heur_maq):
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

            move = games.alphabeta_search(state, game, d=heur_maq.depth, eval_fn=heur_maq.modo)

            state = game.make_move(move, state)
            player = 'O'
        print "-------------------"
        if game.terminal_test(state):
            game.display(state)
            print "Final de la partida"
            break


player = decide_inicio()
game = games.ConnectFour(player=player)
state = game.initial

modo_maquina = heuristicas.Heuristicas("X")

if (decide_jugador2() in ("s", "S", "si", "Si", "SI")):
    maq_maq(game, state, player, modo_maquina, heuristicas.Heuristicas("O"))

else:
    maq_jug(game, state, player, modo_maquina)







