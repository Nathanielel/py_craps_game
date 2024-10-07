import unittest

from game.core import CrapsGame
from game.player import Player
from game.bets.bet_manager import *

class TestCrapsGame(unittest.TestCase):
    def setup(self):
        p1 = Player("Test Player", 100)
        self.game = CrapsGame([p1])

    