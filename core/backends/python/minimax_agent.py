# Agent for Minimax Decisions
# Heuristic inspiration "https://brilliant.org/discussions/thread/artificial-intelligence-for-chain-reaction/"

# ---- SCORE EVALUATION FROM FEATURES -----
# (+/-) Win and Loss
# (+)   Friendly Orb Count
# (-)   Surrounding Enemy Critical Orbs
# (+)   Corner and Edge Cells
# (+)   Critical Safe Orb
# (+)   Critical Non-Orphan Orb
# ------------------------------------
# "friendly" : belonging to player
# "critical" : orb one step away from explosion
# "safe"     : no adjacent critical enemy cells
# "orphan"   : no adjacent critical friendly cells


import core.backends.python.chain_engine as engine


# ------------ UTILITIES -------------
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


def score_minimizer(board, player, alpha, beta) -> int:
    """ Minimizing Score Function """

    # setup
    enemy = 1 - player
    esign = -1 if enemy else 1
    score = 10000

    # searching all valid nodes
    for idx in range(len(board)):

        # skip invalid moves
        if board[idx] * esign < 0:
            continue

        # prune immediately if game over
        cboard = board[:]
        if engine.interact_inplace(cboard, idx, enemy):
            return -10000

        # get child score
        cscore = board_score(cboard, player)

        # update
        score = min(score, cscore)
        beta = min(beta, score)

        # alpha-beta pruning
        if alpha >= beta:
            return score

    return score


def pruned_minimizer(board, player, alpha, beta, depth) -> int:
    """ Minimizing Tree Search Function """

    # setup
    enemy = 1 - player
    esign = -1 if enemy else 1
    score = 10000

    # max depth reached
    if depth == 0:
        return score_minimizer(board, player, alpha, beta)

    # searching all valid nodes
    for idx in range(len(board)):

        # skip invalid moves
        if board[idx] * esign < 0:
            continue

        # prune immediately if game over
        cboard = board[:]
        if engine.interact_inplace(cboard, idx, enemy):
            return -10000

        # get child score
        cscore = pruned_maximizer(cboard, player, alpha, beta, depth)

        # update
        score = min(score, cscore)
        beta = min(beta, score)

        # alpha-beta pruning
        if alpha >= beta:
            return score

    return score


def pruned_maximizer(board, player, alpha, beta, depth) -> int:
    """ Maximizing Tree Search Function """

    # setup
    score = -10000
    psign = -1 if player else 1

    # searching all nodes
    for idx in range(len(board)):

        # skip invalid moves
        if board[idx] * psign < 0:
            continue

        # prune immediately if game over
        cboard = board[:]
        if engine.interact_inplace(cboard, idx, player):
            return 10000

        # update score and beta
        score = max(
            score, pruned_minimizer(cboard, player, alpha, beta, depth - 1)
        )
        alpha = max(alpha, score)

        # alpha-beta pruning
        if alpha >= beta:
            return score

    return score


def load_scores(board, player, depth) -> list:
    """ Get the scores of all moves of board """

    # setup
    alpha = -10000
    psign = -1 if player else 1
    score_list = [0] * len(board)

    # searching all nodes (conditional return inside)
    for idx in range(len(board)):

        # mark invalid moves
        if board[idx] * psign < 0:
            score_list[idx] = -20000
            continue

        # interact with board
        cboard = board[:]
        game_over = engine.interact_inplace(cboard, idx, player)

        # mark winning move (no use of other scores)
        if game_over:
            score_list[idx] = 10000
            return score_list

        # store score and update alpha
        score = pruned_minimizer(cboard, player, alpha, 10000, depth - 1)
        score_list[idx] = score
        alpha = max(alpha, score)

    return score_list
