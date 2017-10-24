from gamestate import *
from minimax_helpers import *
import unittest


class MinimaxHelperTests(unittest.TestCase):
    def test_min_value_WhenEmptyBoard(self):
        g = GameState()

        self.assertEqual(min_value(g), -1)

    def test_terminal_test_WhenNotTerminal(self):
        g = GameState()

        self.assertFalse(terminal_test(g))

    def test_terminal_test_WhenTerminal(self):
        g = GameState()
        terminalState = g.forecast_move((0, 0)).forecast_move((0, 1)).forecast_move((0, 2)) \
            .forecast_move((1, 0)).forecast_move((1, 1))

        self.assertTrue(terminal_test(terminalState))
