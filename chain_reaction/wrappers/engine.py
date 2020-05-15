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
def valid_board_moves(board: list, player: int) -> list:
    """ List of all valid move indices on board for player """

    psign = -1 if player else 1
    return [i for i, b_elem in enumerate(board) if b_elem * psign >= 0]


def interact_inplace(board: list, move: int, player: int) -> bool:
    """
    Interact with Chain Reaction Environment
    Modifies board inplace
    Note: Does not check if game was over, do checking outside
    """

    # setup
    psign = -1 if player else 1
    game_over = False

    # using queue to sequentialize steps
    # near cells are calculated first
    work = queue.Queue()
    work.put(move)

    # store counts
    pos, neg = 0, 0
    for elem in board:
        pos += elem > 0
        neg += elem < 0

    # swap counts if player is 1
    t_frn, t_enm = (neg, pos) if player else (pos, neg)

    while not (work.empty() or game_over):
        # get next index in queue
        idx = work.get()

        # update territory count and game over flag
        t_frn += 1
        t_enm -= board[idx] * psign < 0
        game_over = (t_frn + t_enm > 2) and (t_enm == 0)

        # update orb count according to rule
        orbct = abs(board[idx]) + 1
        maxcp = len(NTABLE[idx])
        board[idx] = (orbct % maxcp) * psign

        # append next indices if exploded
        if orbct == maxcp:
            [work.put(i) for i in NTABLE[idx]]

    return game_over


def interact_onestep(board: list, moves: list, player: int) -> tuple:
    """
    Interact with chain reaction Environment in steps
    Returns (next_moves, explosions, game_over)
    """

    # setup
    psign = -1 if player else 1
    next_moves = []
    explosions = []

    # first pass increments all cells
    for move in moves:
        board[move] = (abs(board[move]) + 1) * psign

    # second pass gets all explosions (ignoring duplicates)
    for move in set(moves):
        # update orb count
        orbct = abs(board[move])
        maxcp = len(NTABLE[move])
        board[move] = (orbct % maxcp) * psign

        # explosion condition
        if orbct >= maxcp:
            explosions.append(move)

            # see if neighbor is stable
            for neighbor in NTABLE[move]:
                ncount = (abs(board[neighbor]) + 1) % len(NTABLE[neighbor])

                # append only unstable moves, else save final state
                if ncount == 0:
                    next_moves.append(neighbor)
                else:
                    board[neighbor] = (abs(board[neighbor]) + 1) * psign

    # store counts
    pos, neg = 0, 0
    for elem in board:
        pos += elem > 0
        neg += elem < 0

    # swap counts if player is 1
    t_frn, t_enm = (neg, pos) if player else (pos, neg)

    # update even next moves
    for nmove in next_moves:
        t_frn += 1
        t_enm -= board[nmove] * psign < 0

    # if game is mature and any one is zero, game is over
    game_over = (t_frn + t_enm > 2) and (t_enm <= 0)
    return (next_moves, explosions, game_over)


def interact_view(board: list, move: int, player: int) -> tuple:
    """
    Interact with Chain Reaction Environment
    Returns view of outcome
    """

    board_dupl = board[:]
    gmovr = interact_inplace(board_dupl, move, player)

    return (board_dupl, gmovr)


# ----------- CLASSES --------------
class ChainReactionGame:
    def __init__(self):
        """ Chain Reaction Game Engine """
        assert SHAPE, "Game Engine Module Not Initialized"

        # game state
        self.board = [0] * SHAPE[0] * SHAPE[1]
        self.player = 0

        # outcome
        self.game_over = False
        self.winner = 2

    def make_move(self, move) -> bool:
        """
        Calculate the next state of the board
        -------------------------------------
        Input   : move index (tuple or int)
        Returns : success boolean
        """

        # setup
        index = move if type(move) is int else move[0] * SHAPE[1] + move[1]
        psign = -1 if self.player else 1

        # invalid condition
        if (self.board[index] * psign < 0) or self.game_over:
            return False

        # interact inplace
        self.game_over = interact_inplace(self.board, index, self.player)
        self.winner = self.player if self.game_over else 2

        # toggle player
        self.player = 1 - self.player
        return True


class ChainReactionAnimated:
    def __init__(self):
        """ Chain Reaction Animation Engine """
        assert SHAPE, "Game Engine Module Not Initialized"

        # game state
        self.board = [0] * SHAPE[0] * SHAPE[1]
        self.player = 0

        # intermediate states
        self.pending_moves = []

        # outcome
        self.game_over = False
        self.winner = 2

    def make_move(self, move) -> bool:
        """
        Start a move on board
        Returns True if successful
        Note: Call get_next_step repeatedly until board is stable
        """
        # setup
        index = move if type(move) is int else move[0] * SHAPE[1] + move[1]
        psign = -1 if self.player else 1

        # invalid condition
        if (self.board[index] * psign < 0) or self.game_over:
            return False

        self.pending_moves = [index]
        return True

    def get_next_step(self) -> tuple:
        """
        Calculate state of the board in steps
        Returns (previous board, exploded indices)
        Note: To be called repeatedly until exhausted after make_move
        """

        # invalid call -> return None tuple
        if not self.pending_moves:
            return (None, None)

        # save previous board for animation
        previous_board = self.board[:]
        res = interact_onestep(self.board, self.pending_moves, self.player)

        # unpack res and update
        self.pending_moves, explosions, self.game_over = res
        self.winner = self.player if self.game_over else 2

        # update player if stable
        if not self.pending_moves:
            self.player = 1 - self.player

        return (previous_board, explosions)
