# The On Init and Init sections contain variables and functors,
# which will be modified by init function depending on backends.
# The sole reason of their existance is to keep the linter happy.


import random
import core.wrappers.engine as engine


# ---------- ON INIT ---------------
minimizer = None
maximizer = None


# ----------- INIT -----------------
def init(backend):

    global minimizer, maximizer

    # setting up python engine
    if backend == "python":
        import core.backends.python.minimax_agent as pagent
        minimizer = pagent.pruned_minimizer
        maximizer = pagent.pruned_maximizer

    # setting up c engine
    elif backend == "c":
        import core.backends.c_ext.minimax_agent as cagent
        minimizer = cagent.pruned_minimizer
        maximizer = cagent.pruned_maximizer
    
    # error
    else:
        raise ValueError("only c and python backends supported")


# ------- WRAPPER FUNCTIONS --------
def move_chooser(board: list, player: int, depth, samples) -> int:
    """
    Get weighted random choice of best moves for the player
    -------------------------------------------------------
    If there is an immediate winning move, always return it
    board   : state of game where the choice has to be made
    player  : player id corresponding to the deciding agent
    depth   : every increment adds both max and mini levels
    samples : the top n moves which will be chosen randomly
    """

    # setup
    heatmap = []
    psign = -1 if player else 1
    alpha = -10000

    # safety
    if depth <= 0:
        raise ValueError("minimax search depth has to be greater than zero")
    if depth > 2:
        raise ValueError("raising depth above 2 is terribly slow")

    # store values for sorting
    for idx in range(engine.SHAPE[0] * engine.SHAPE[1]):

        # skip invalid move
        if board[idx] * psign < 0:
            continue

        # return winning move immediately
        nboard, gmovr = engine.interact_view(board, idx, player)
        if gmovr:
            return idx

        # store score and alpha
        score = minimizer(nboard, player, alpha, 10000, depth - 1)
        alpha = max(alpha, score)
        heatmap.append((idx, score))

    # get random move with scores as weights
    # if score difference is high, probability of selection is low
    heatmap.sort(key=lambda x: x[1], reverse=True)
    m_moves = [i[0] for i in heatmap[:samples] if i[1] > 0]
    weights = [6, 4, 2, 1, 1][:len(m_moves)]

    # return random choice if more than one score is positive
    # otherwise, return the move with highest score
    if len(m_moves) > 1:
        return random.choices(m_moves, weights)[0]
    else:
        return heatmap[0][0]
