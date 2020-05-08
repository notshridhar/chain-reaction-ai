# The On Init and Init sections contain variables and functors,
# which will be modified by init function depending on backends.
# The sole reason of their existance is to keep the linter happy.


# ---------- ON INIT ---------------
SHAPE = None
interact_inplace = None


# ----------- INIT -----------------
def init(shape, backend):
    global SHAPE
    global interact_inplace

    # setting up python engine
    if backend == "python":
        import core.backends.python.chain_engine as pengine

        SHAPE = shape
        pengine.init(shape=shape)
        interact_inplace = pengine.interact_inplace

    # setting up c engine
    else:
        import core.backends.c_ext.chain_engine as cengine

        if shape != (9, 6):
            print("C Backend can only support 9 x 6 game")
            print("Playing on 9 x 6 grid")
        SHAPE = (9, 6)
        interact_inplace = cengine.interact_inplace


# ------- WRAPPER FUNCTIONS --------
def interact_view(board: list, move: int, plrid: int):
    """
    Interact with Chain Reaction Environment
    Returns view of outcome
    """

    board_dupl = board[:]
    gmovr = interact_inplace(board_dupl, move, plrid)

    return (board_dupl, gmovr)


# ----------- CLASSES --------------
class GameEngine(object):
    def __init__(self):
        """ Chain Reaction Game Engine """
        assert SHAPE, "Game Engine Module Not Initialized"

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
        idx = move if type(move) is int else move[0] * SHAPE[1] + move[1]
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
