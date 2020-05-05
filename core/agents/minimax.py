# Agent for Minimax Decisions
# Heuristic from "https://brilliant.org/discussions/thread/artificial-intelligence-for-chain-reaction/"

# -------- HEURISTIC FUNCTION --------
# 1. If player wins, score is 10000, else if the enemy wins, score is -10000.
# 2. For friendly orb, add 1 to the value.
# 3. For friendly orb, subtract 5 - critical mass of orb for every surrounding enemy critical cell.
# 4. For friendly safe orb, add 2 (edge cell) or 3 (corner cell).
# 5. For friendly critical safe orb, add 2 to the value.
# 6. For friendly critical non-orphan orb, add twice the number of cells to the score.
# ------------------------------------
# "friendly" : orb belonging to player
# "critical" : orb one step away from explosion
# "safe"     : orb with no adjacent critical enemy cells
# "orphan"   : orb with no adjacent critical friendly cells


import random
import core.engine as engine


# ------------ UTILITIES -------------
def moves_list(board, player) -> list:
    """ Get list of all valid moves for player on board """
    psign = -1 if player else 1
    return [i for i, orb in enumerate(board) if orb * psign >= 0]


def board_score(board, player) -> int:
    """ Calculate board score in favor of player """
    # setup
    size = len(board)
    psign = -1 if player else 1
    ntable = engine.NTABLE
    total_score = 0

    # cache tables for quick lookups
    en_crit = [board[x] * psign == 1 - len(ntable[x]) for x in range(size)]
    fr_crit = [board[x] * psign == len(ntable[x]) - 1 for x in range(size)]

    for idx in range(size):
        # multiplying psign makes player territories positive
        plr_orbs = board[idx] * psign

        # player territory
        if plr_orbs > 0:
            # assign to local variable
            neighbrs = ntable[idx]
            is_critc = fr_crit[idx]
            maxcp = len(neighbrs)

            # number of surrounding critical enemies and friends
            crit_enemies = sum([en_crit[nid] for nid in neighbrs])
            crit_friends = sum([fr_crit[nid] for nid in neighbrs])

            # RULE 2 and RULE 3
            total_score += plr_orbs
            total_score -= (5 - maxcp) * crit_enemies

            # RULE 4 and RULE 5
            if not crit_enemies:
                total_score += 3 if maxcp == 2 else 0
                total_score += 2 if maxcp == 3 else 0
                total_score += 2 if is_critc else 0

            # RULE 6
            if is_critc and crit_friends:
                total_score += 2

    return total_score


def minimizer(board, player, alpha, beta, depth) -> int:
    """ Minimizing Tree Search Function """

    # setup
    interact = engine.interact_view
    enemy = 1 - player
    score = 10000

    # searching all nodes
    for move in moves_list(board, enemy):

        # prune immediately if game over
        cboard, gmovr = interact(board, move, enemy)
        if gmovr:
            return -10000

        # get child score
        if depth:
            cscore = maximizer(cboard, player, alpha, beta, depth)
        else:
            cscore = board_score(cboard, player)

        # update
        score = min(score, cscore)
        beta = min(beta, score)

        # alpha-beta pruning
        if alpha >= beta:
            break

    return score


def maximizer(board, player, alpha, beta, depth) -> int:
    """ Maximizing Tree Search Function """

    # setup
    interact = engine.interact_view
    score = -10000

    # searching all nodes
    for move in moves_list(board, player):

        # prune immediately if game over
        cboard, gmovr = interact(board, move, player)
        if gmovr:
            return 10000

        # update score and beta
        score = max(score, minimizer(cboard, player, alpha, beta, depth - 1))
        alpha = max(alpha, score)

        # alpha-beta pruning
        if alpha >= beta:
            break

    return score


def move_chooser(board: list, player: int, depth=1, samples=3) -> int:
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
    interct = engine.interact_view
    movlist = moves_list(board, player)
    heatmap = [0] * len(movlist)
    alpha = -10000

    # store values for sorting
    for i, move in enumerate(movlist):

        # return winning move immediately
        nboard, gmovr = interct(board, move, player)
        if gmovr:
            return move

        # store score and alpha
        score = minimizer(nboard, player, alpha, 10000, depth - 1)
        alpha = max(alpha, score)
        heatmap[i] = (move, score)

    # get random move with scores as weights
    # if score difference is high, probability of selection is low
    heatmap.sort(key=lambda x: x[1], reverse=True)
    bestmoves = [i[0] for i in heatmap[:samples] if i[1] > 0]
    bestscore = [i[1] for i in heatmap[:samples] if i[1] > 0]

    # return random choice if more than one score is positive
    # otherwise, return the move with highest score
    if len(bestmoves) > 1:
        return random.choices(bestmoves, bestscore)[0]
    else:
        return heatmap[0][0]
