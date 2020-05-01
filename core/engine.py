# The base engine driving Chain Reactions
# Handles all the logic for the game
# Implemented in pure python for performance

from queue import Queue


# --------- ON INIT --------------
DIMENSION = None
NEIGH_TABLE = None


# -------- INIT ---------
def init(shape=(9, 6)):
    """ Preliminary stuff (caching) """
    global DIMENSION, NEIGH_TABLE

    DIMENSION = shape
    NEIGH_TABLE = create_neighbor_table(shape)


# -------- INSIDE JOBS ---------------
def territory_count(state, plrid):
    """ Return territory counts (player, opponent) """
    one, two = 0, 0
    for elem in state:
        one += elem < 0
        two += elem > 0
    return (one, two) if plrid else (two, one)


def create_neighbor_table(shape):
    """ Store neighboring indices for quick lookup """
    s_h, s_w = shape
    n_table = [0] * s_w * s_h
    for idx in range(s_h * s_w):
        i_y, i_x = idx // s_w, idx % s_w
        temp = [
            idx - s_w if i_y > 0 else None,
            idx + s_w if i_y < s_h - 1 else None,
            idx - 1 if i_x > 0 else None,
            idx + 1 if i_x < s_w - 1 else None,
        ]
        n_table[idx] = tuple(filter(None.__ne__, temp))
    return tuple(n_table)


# ------- INTERACTION FUNCTIONS -------------
def interact_copy(state: list, move: int, plrid: int):
    """
    Interact with Chain Reaction Environment
    Returns copied state and does not modify state inplace
    Slightly slower because of copying
    """

    state_dupl = state[:]
    gmovr, winnr = interact_inplace(state_dupl, move, plrid)

    return (state_dupl, gmovr, winnr)


def interact_inplace(state: list, move: int, plrid: int):
    """
    Interact with Chain Reaction Environment
    Modifies state inplace
    """

    # using queue to sequentialize steps
    # near cells are calculated first
    stpq = Queue()
    stpq.put(move)

    t_one, t_two = territory_count(state, plrid)
    psign = [1, -1][plrid]
    gmovr = False

    while not (stpq.empty() or gmovr):
        # get next index
        idx = stpq.get()

        # update territory counts and game over
        t_one += 1
        t_two -= state[idx] * psign < 0
        gmovr = (t_one + t_two > 2) and (t_one * t_two == 0)

        # update cell count
        ccount = abs(state[idx]) + 1
        max_cp = len(NEIGH_TABLE[idx])
        state[idx] = (ccount % max_cp) * psign

        # explode and append next indices
        if ccount == max_cp:
            list(map(stpq.put, NEIGH_TABLE[idx]))

    winnr = [1, 2][plrid] * (t_two == 0) * gmovr
    return (gmovr, winnr)


# -------- SEQUENTIAL GAME CLASS ------------------
class GameEngine(object):
    def __init__(self):
        """ Chain Reaction Game Engine """

        # warn if not init
        assert DIMENSION, "Game Engine not initialized"

        # game state
        self.state = [0] * DIMENSION[0] * DIMENSION[1]
        self.plrid = 0

        # outcome
        self.gmovr = False
        self.winnr = 0

    def fast_play(self, move: tuple) -> bool:
        """
        Calculate the state of the board
        Input   : move index tuple
        Returns : success boolean
        <- direct output without intermediate steps ->
        """

        # flatten index
        idx = move[0] * DIMENSION[1] + move[1]

        # invalid condition
        psign = [1, -1][self.plrid]
        if self.gmovr or (self.state[idx] * psign < 0):
            return False

        # interact inplace
        status = interact_inplace(self.state, idx, self.plrid)
        self.gmovr, self.winnr = status

        # toggle player
        self.plrid = 1 - self.plrid
        return True
