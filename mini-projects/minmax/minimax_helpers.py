def terminal_test(gameState):
    """ Return True if the game is over for the active player
    and False otherwise.
    """
    return not any(gameState.get_legal_moves())


def min_value(gameState):
    """ Return the value for a win (+1) if the game is over,
    otherwise return the minimum value over all legal child
    nodes.
    """
    if terminal_test(gameState):
        return 1

    return min(map(lambda m: max_value(gameState.forecast_move(m)), gameState.get_legal_moves()))


def max_value(gameState):
    """ Return the value for a loss (-1) if the game is over,
    otherwise return the maximum value over all legal child
    nodes.
    """
    if terminal_test(gameState):
        return -1

    return max(map(lambda m: min_value(gameState.forecast_move(m)), gameState.get_legal_moves()))
