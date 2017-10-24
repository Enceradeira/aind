from gamestate import *
import unittest


class GameStateTests(unittest.TestCase):
    def test_get_initial_moves(self):
        state = GameState()

        moves = state.get_legal_moves()

        self.assertEqual(moves, [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1)])

    def test_DIRECTIONS_ShouldReturn8Directions(self):
        uniq_directions = set(GameState.DIRECTIONS)
        self.assertEqual(len(uniq_directions), 8)

    def test_DIRECTIONS_ShouldContainDirections(self):
        self.assertTrue((1, 1) in GameState.DIRECTIONS)
        self.assertFalse((0, 0) in GameState.DIRECTIONS)

    def test_get_legal_moves_WhenExample1(self):
        s1 = GameState()
        # Player A moves
        s2 = s1.forecast_move((1, 1))
        self.assertEqual(s2.get_legal_moves(), [(0, 0), (1, 0), (2, 0), (0, 1)])

        # Player B moves
        s3 = s2.forecast_move((0, 1))
        self.assertEqual(s3.get_legal_moves(), [(0, 0), (1, 0), (2, 0)])

        # Player A moves
        s4 = s3.forecast_move((0, 0))
        self.assertEqual(s4.get_legal_moves(), [(1, 0)])

        # Player B moves
        s5 = s4.forecast_move((1, 0))
        self.assertEqual(s5.get_legal_moves(), [])

    def test_get_legal_moves_WhenExample2(self):
        s1 = GameState()
        # Player A moves
        s2 = s1.forecast_move((0, 0))
        self.assertEqual(s2.get_legal_moves(), [(1, 0), (2, 0), (0, 1), (1, 1)])

        # Player B moves
        s3 = s2.forecast_move((0, 1))
        self.assertEqual(s3.get_legal_moves(), [(1, 0), (2, 0), (1, 1)])

        # Player A moves
        s4 = s3.forecast_move((1, 0))
        self.assertEqual(s4.get_legal_moves(), [(1, 1)])

        s5 = s4.forecast_move((1, 1))
        self.assertEqual(s5.get_legal_moves(), [(2, 0)])

        # Player A moves
        s6 = s5.forecast_move((2, 0))
        self.assertEqual(s6.get_legal_moves(), [])
