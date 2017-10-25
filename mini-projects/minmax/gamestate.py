import copy


class GameState:
    def create_indicies(board):
        return [(column, row) for row in range(0, len(board)) for column in range(0, len(board[0]))]

    def get_max_index(selector, indicies):
        return max(map(lambda x: selector(x), indicies))

    INITIAL_BOARD = [[False, False, False], [False, False, True]]

    DIRECTIONS = [d for d in [(c, r) for c in range(-1, 2) for r in range(-1, 2)] if d != (0, 0)]

    INDICES = create_indicies(INITIAL_BOARD)

    MAX_COLUMN_INDEX = get_max_index(lambda x: x[0], INDICES)

    MAX_ROW_INDEX = get_max_index(lambda x: x[1], INDICES)

    PLAYER_MAX = 'MAX'

    PLAYSER_MIN = 'MIN'

    def __init__(self):
        self._board = GameState.INITIAL_BOARD
        self._player_to_move = GameState.PLAYER_MAX
        self._player_max_position = None
        self._player_min_position = None
        return

    def _set_new_turn(self, move):
        if self._player_to_move == GameState.PLAYER_MAX:
            self._player_to_move = GameState.PLAYSER_MIN
            self._player_max_position = move
        else:
            self._player_to_move = GameState.PLAYER_MAX
            self._player_min_position = move

    def _get_current_position(self):
        if self._player_to_move == GameState.PLAYER_MAX:
            return self._player_max_position
        else:
            return self._player_min_position

    def _get_cell_state(self, coordinate):
        return self._board[coordinate[1]][coordinate[0]]

    def _set_new_state(self, move, value):
        self._board[move[1]][move[0]] = value
        self._set_new_turn(move)

    def _increment_vectors(self, vector):
        for v in vector:
            x = v[0]
            y = v[1]
            _x = (int)(x / abs(x)) * (abs(x) + 1) if x != 0 else 0
            _y = (int)(y / abs(y)) * (abs(y) + 1) if y != 0 else 0
            yield (_x, _y)

    def _get_possible_moves_from_players_position(self, directions):
        """ Returns the possible moves to cells with a certain distance

        :param distance: distance of cell from current players position
        :return: moves as tuple of direction (vector) and new absolute position [(0,1),(0,2]]
        """
        players_position = self._get_current_position()

        # moves include those that leave the board
        all_moves = [m for m in map(lambda d: ((d), (players_position[0] + d[0], players_position[1] + d[1])),
                                    directions)]

        # moves within board including cells that are already taken
        max_col_index = GameState.MAX_COLUMN_INDEX
        max_row_index = GameState.MAX_ROW_INDEX
        potential_moves = [m for m in all_moves if (0 <= m[1][0] <= max_col_index) and (0 <= m[1][1] <= max_row_index)]

        # moves within board excluding taken cells
        moves = [m for m in potential_moves if not self._get_cell_state(m[1])]

        if (any(moves)):
            # maybe we can move further than given distance
            available_directions = self._increment_vectors(map(lambda t: t[0], moves))
            return moves + self._get_possible_moves_from_players_position(available_directions)

        return moves

    def forecast_move(self, move):
        """ Return a new board object with the specified move
        applied to the current game state.

        Parameters
        ----------
        move: tuple
            The target position for the active player's next move
        """
        new_board = copy.deepcopy(self)
        new_board._set_new_state(move, True)
        return new_board

    def get_legal_moves(self):
        """ Return a list of all legal moves available to the
        active player.  Each player should get a list of all
        empty spaces on the board on their first move, and
        otherwise they should get a list of all open spaces
        in a straight line along any row, column or diagonal
        from their current position. (Players CANNOT move
        through obstacles or blocked squares.) Moves should
        be a pair of integers in (column, row) order specifying
        the zero-indexed coordinates on the board.
        """

        if not self._get_current_position():
            # return initially available moves
            return [i for i in GameState.INDICES if not self._get_cell_state(i)]
        else:
            unorderd_result = map(lambda t: t[1], self._get_possible_moves_from_players_position(GameState.DIRECTIONS))
            return list(sorted(unorderd_result, key=lambda x: (x[1], x[0])))
