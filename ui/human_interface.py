from game.core import CrapsGame
from game.player import Player

def start_human_game():

    name = input("Enter your name: ")
    bal = input("Enter your starting bankroll (default 1000): ")
    player = Player(name, bal)
    game = CrapsGame([player])
    game.run()

def join_human_game():
    print("WARNING: NOT IMPLEMENTED")

def add_human_player(game):
    print("WARNING: NOT IMPLEMENTED")
