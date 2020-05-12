# The On Init and Init sections contain variables and functors,
# which will be modified by init function depending on backends.
# The sole reason of their existance is to keep the linter happy.


# ---------- ON INIT ---------------
best_action = None


# ----------- INIT -----------------
def init(backend):

    global best_action

    import core.backends.python.mcts_agent as pagent

    best_action = pagent.best_action


# ------- WRAPPER FUNCTIONS --------
def best_move(board: list, player: int, time_limit: float, c_param=1.4) -> int:
    """
    Get best move from Monte Carlo Tree Search Method
    Returns within time limit
    """

    # direct redirect to backend
    return best_action(board, player, time_limit, c_param)

