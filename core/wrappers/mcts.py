import core.backends.python.mcts_agent as mcts


# ------- WRAPPER FUNCTIONS --------
def best_move(board: list, player: int, time_limit: float, c_param=1.4) -> int:
    """
    Get best move from Monte Carlo Tree Search Method
    Returns within time limit
    """

    # redirect to backend
    return mcts.best_action(board, player, time_limit, c_param)

