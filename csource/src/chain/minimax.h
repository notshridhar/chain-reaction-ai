#ifndef MINIMAX_AGENT_H
#define MINIMAX_AGENT_H


/**
 * Minimax Minimizer Level (RECURSIVE)
 * -----------------------------------
 * integrated alpha-beta pruning
 * if depth is zero, returns minimized static evaluation score
 * else returns minimized score from lower depths
 */
int
minimax__pruned_minimizer ( int  *board,
                            int   player,
                            int   alpha,
                            int   beta,
                            int   depth );


/**
 * Minimax Maximizer Level (RECURSIVE)
 * -----------------------------------
 * integrated alpha-beta pruning
 * depth should never be zero
 * returns maximized score of lower depths
 */
int
minimax__pruned_maximizer ( int  *board,
                            int   player,
                            int   alpha,
                            int   beta,
                            int   depth );


#endif