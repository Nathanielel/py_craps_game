import unittest

from game.core import CrapsGame
from game.player import HumanPlayer
from game.bets.bet_manager import *

class TestCrapsGame(unittest.TestCase):
    
    def setUp(self):
        self.p1 = HumanPlayer("Test Player", 100)
        self.game = CrapsGame([self.p1])
    
    def test_cashout(self):
        self.p1.cashing_out = True
        self.assertEqual(100, self.game.players[0].balance)
