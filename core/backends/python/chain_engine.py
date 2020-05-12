# The base engine driving Chain Reactions
# Contains the bare minimum logic functions


import queue


# ---------- ON INIT ---------------
SHAPE = None
NTABLE = None


# ----------- INIT -----------------
def init(shape):
    """ Calculate variables and cache tables """
    global SHAPE, NTABLE

    # store shape
    SHAPE = shape

    # store neighbor indices as tuple of tuples
    s_h, s_w = shape
    NTABLE = [0] * s_w * s_h
    for idx in range(s_h * s_w):
        i_y, i_x = idx // s_w, idx % s_w
        temp = [
            idx - s_w if i_y > 0 else None,
            idx + s_w if i_y < s_h - 1 else None,
            idx - 1 if i_x > 0 else None,
            idx + 1 if i_x < s_w - 1 else None,
        ]
        NTABLE[idx] = tuple([i for i in temp if i is not None])
    NTABLE = tuple(NTABLE)


# --------- CORE FUNCTIONS ------------
def valid_board_moves(board: list, player) -> list:
    """ List of all valid move indices on board for player """
    psign = -1 if player else 1
    return [i for i, b_elem in enumerate(board) if b_elem * psign >= 0]


def interact_inplace(board: list, move: int, plrid: int) -> bool:
    """
    Interact with Chain Reaction Environment
    Modifies board inplace
    Note: Does not check if game was over, do checking outside
    """

    # setup
    ntable = NTABLE
    psign = -1 if plrid else 1
    game_over = False

    # using queue to sequentialize steps
    # near cells are calculated first
    work = queue.Queue()
    work.put(move)

    # store counts (friend, enemy)
    t_frn, t_enm = 0, 0
    for elem in board:
        t_frn += elem > 0
        t_enm += elem < 0

    # swap counts if plrid is 1
    t_frn, t_enm = (t_enm, t_frn) if plrid else (t_frn, t_enm)

    while not (work.empty() or game_over):
        # get next index in queue
        idx = work.get()

        # update territory counts and game over flag
        t_frn += 1
        t_enm -= board[idx] * psign < 0
        game_over = (t_enm + t_frn > 2) and (t_enm * t_frn == 0)

        # update orb count according to rule
        orbct = abs(board[idx]) + 1
        maxcp = len(ntable[idx])
        board[idx] = (orbct % maxcp) * psign

        # append next indices if exploded
        if orbct == maxcp:
            [work.put(i) for i in ntable[idx]]

    return game_over
