import games
import random

modos = ["modo_facil", "modo_medio", "modo_dificil"]
auxHeur = []

def modo_facil():
    return random.randint(0, 20)

def display_heuristicas():
    return "Heuristicas disponibles"

    i = 0
    for h in heuristicas:
        print "(" + i+1 + ")" + h
        i+=1

def get_modo(i):
    return modos[i]

def get_auxHeur(i):
    return auxHeur[i]

def get_auxHeur_length():
    return len(auxHeur)