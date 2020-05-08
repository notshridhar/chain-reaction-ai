#include "chain/engine.h"
#include "chain/minimax.h"


/* Critical Mass Lookup Table */
static char NTABLE [9 * 6] = {
    2, 3, 3, 3, 3, 2,
    3, 4, 4, 4, 4, 3,
    3, 4, 4, 4, 4, 3,
    3, 4, 4, 4, 4, 3,
    3, 4, 4, 4, 4, 3,
    3, 4, 4, 4, 4, 3,
    3, 4, 4, 4, 4, 3,
    3, 4, 4, 4, 4, 3,
    2, 3, 3, 3, 3, 2,
};


/* Heuristic Evaluation Functions (in favor of player) */
static int WIN_SCORE = +10000;
static int LOS_SCORE = -10000;

static int
minimax__evaluation_score ( int  *board,
                            int   player )
{
    int psign = player ? -1 : 1;
    int score = 0;

    int c_frn_arr[54];
    int c_enm_arr[54];

    /* critical friends and enemy table */
    for (int i = 0; i < 54; ++i)
    {
        c_frn_arr[i] = ((board[i] * psign) == (NTABLE[i] - 1));
        c_enm_arr[i] = ((board[i] * psign) == (1 - NTABLE[i]));
    }

    for (int i = 0; i < 54; ++i)
    {
        int plr_orbs = board[i] * psign;

        /* skip enemy and empty territory */
        if (plr_orbs <= 0)
            continue;

        /* Critical friends and enemies */
        int crit_frn = 0;
        int crit_enm = 0;

        /* count surrounding enemies and friends */
        int i_y = i / 6;
        int i_x = i % 6;

        if (i_y > 0)
        {
            if (c_frn_arr[i - 6]) ++crit_frn;
            if (c_enm_arr[i - 6]) ++crit_enm;
        }
        if (i_y < 8)
        {
            if (c_frn_arr[i + 6]) ++crit_frn;
            if (c_enm_arr[i + 6]) ++crit_enm;
        }
        if (i_x > 0)
        {
            if (c_frn_arr[i - 1]) ++crit_frn;
            if (c_enm_arr[i - 1]) ++crit_enm;
        }
        if (i_x < 5)
        {
            if (c_frn_arr[i + 1]) ++crit_frn;
            if (c_enm_arr[i + 1]) ++crit_enm;
        }

        score += plr_orbs;
        score -= crit_enm * (5 - NTABLE[i]);

        if (crit_enm == 0)
        {
            if (NTABLE[i] == 2)             score += 3;
            if (NTABLE[i] == 3)             score += 2;
            if (NTABLE[i] == plr_orbs + 1)  score += 2;
        }

        if ((NTABLE[i] == plr_orbs + 1) && (crit_frn > 0))
            score += 2;
    }

    return score;
}


/* Direct Evaluation Minimizer Level */
int
minimax__score_minimizer  ( int  *board,
                            int   player,
                            int   alpha,
                            int   beta )
{
    /* Assume worst case score and improve */
    int score = WIN_SCORE;
    int enemy = 1 - player;
    int esign = enemy ? -1 : 1;
    int new_board[54];

    /* no more depth to explore */
    for (int i = 0; i < 54; ++i)
    {
        /* skip invalid moves (of enemy) */
        if (board[i] * esign < 0)
            continue;

        /* Interact with environment (enemy) */
        /* Node search is done if game over */
        if (engine__interact(board, new_board, i, enemy))
            return LOS_SCORE;
        
        /* Get recursive score and minimize score and beta */
        int child_score = minimax__evaluation_score(new_board, player);
        score = (child_score < score) ? child_score : score;
        beta  = (beta < score) ? beta : score;

        /* Node search is done if alpha >= beta */
        if (alpha >= beta)
            return score;
    }

    /* Return after search is completed */
    return score;
}


/* Minimax Minimizer Level (RECURSIVE) */
int
minimax__pruned_minimizer ( int  *board,
                            int   player,
                            int   alpha,
                            int   beta,
                            int   depth )
{
    /* Assume worst case score and improve */
    int score = WIN_SCORE;
    int enemy = 1 - player;
    int esign = enemy ? -1 : 1;
    int new_board[54];

    /* maximum depth reached => return min of scores instead */
    if (depth == 0)
        return minimax__score_minimizer(board, player, alpha, beta);

    /* more depth to explore */
    for (int i = 0; i < 54; ++i)
    {
        /* skip invalid moves (of enemy) */
        if (board[i] * esign < 0)
            continue;

        /* Interact with environment (enemy) */
        /* Node search is done if game over */
        if (engine__interact(board, new_board, i, enemy))
            return LOS_SCORE;
        
        /* Get recursive score and minimize score and beta */
        int child_score = minimax__pruned_maximizer(new_board, player, alpha, beta, depth);
        score = (child_score < score) ? child_score : score;
        beta  = (beta < score) ? beta : score;

        /* Node search is done if alpha >= beta */
        if (alpha >= beta)
            return score;
    }

    /* Return after search is completed */
    return score;
}


/* Minimax Maximizer Level (RECURSIVE) */
int
minimax__pruned_maximizer ( int  *board,
                            int   player,
                            int   alpha,
                            int   beta,
                            int   depth )
{
    /* Assume worst case score and improve */
    int score = LOS_SCORE;
    int psign = player ? -1 : 1;
    int new_board[54];

    /* more depth to explore */
    for (int i = 0; i < 54; ++i)
    {
        /* skip invalid moves */
        if (psign * board[i] < 0)
            continue;

        /* Node search is done if game over */
        if (engine__interact(board, new_board, i, player))
            return WIN_SCORE;
        
        /* Get recursive score and maximize score and alpha */
        int child_score = minimax__pruned_minimizer(new_board, player, alpha, beta, depth - 1);
        score = (child_score > score) ? child_score : score;
        alpha = (alpha > score) ? alpha : score;

        /* Node search is done if alpha >= beta */
        if (alpha >= beta)
            return score;
    }

    /* Return after search is completed */
    return score;
}