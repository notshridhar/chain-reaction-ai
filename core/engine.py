# The base engine driving Chain Reactions
# Handles all the logic for the game


import queue


# ---------- ON INIT ---------------
SHAPE = None
NTABLE = None


# ----------- INIT -----------------
def init(shape=(9, 6)):
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


# ---------- HELPERS ---------------
def territory_count(board, plrid) -> tuple:
    """ Get territory counts (player, enemy) """
    one, two = 0, 0
    for elem in board:
        one += elem < 0
        two += elem > 0
    return (one, two) if plrid else (two, one)


# --------- INTERACTION ------------
def interact_view(board: list, move: int, plrid: int):
    """
    Interact with Chain Reaction Environment
    Returns view of outcome
    """

    board_dupl = board[:]
    gmovr = interact_inplace(board_dupl, move, plrid)

    return (board_dupl, gmovr)


def interact_inplace(board: list, move: int, plrid: int):
    """
    Interact with Chain Reaction Environment
    Modifies board inplace
    """

    # setup
    ntable = NTABLE
    psign = -1 if plrid else 1
    gmovr = False

    # using queue to sequentialize steps
    # near cells are calculated first
    work = queue.Queue()
    work.put(move)

    # store counts (friend, enemy)
    t_frn, t_enm = territory_count(board, plrid)

    while not (work.empty() or gmovr):
        # get next index in queue
        idx = work.get()

        # update territory counts and game over flag
        t_frn += 1
        t_enm -= board[idx] * psign < 0
        gmovr = (t_enm + t_frn > 2) and (t_enm * t_frn == 0)

        # update orb count according to rule
        orbct = abs(board[idx]) + 1
        maxcp = len(ntable[idx])
        board[idx] = (orbct % maxcp) * psign

        # append next indices if exploded
        if orbct == maxcp:
            [work.put(i) for i in ntable[idx]]

    return gmovr


# ---------- GAME CLASS ------------
class GameEngine(object):
    def __init__(self):
        """ Chain Reaction Game Engine """

        # error if not init
        assert SHAPE, "Game Engine not initialized"

        # game state
        self.board = [0] * SHAPE[0] * SHAPE[1]
        self.plrid = 0

        # outcome
        self.gmovr = False
        self.winnr = 2

    def fast_play(self, move) -> bool:
        """
        Calculate the next state of the board
        -------------------------------------
        Input   : move index (tuple or int)
        Returns : success boolean
        """

        # setup
        idx = move[0] * SHAPE[1] + move[1] if type(move) == tuple else move
        psign = -1 if self.plrid else 1

        # invalid condition
        if (self.board[idx] * psign < 0) or self.gmovr:
            return False

        # interact inplace
        self.gmovr = interact_inplace(self.board, idx, self.plrid)
        self.winnr = self.plrid if self.gmovr else 2

        # toggle player
        self.plrid = 1 - self.plrid
        return True
