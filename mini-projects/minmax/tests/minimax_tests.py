from minimax import *
from gamestate import *
import unittest


class MinimaxDecisionTests(unittest.TestCase):
    def test_minimax_decision(self):
        rootNode = GameState()

        best_move = minimax_decision(rootNode)

        self.assertTrue(best_move in set([(0, 0), (2, 0), (0, 1)]))
