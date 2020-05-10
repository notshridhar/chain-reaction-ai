#ifndef MINIMAX_AGENT_H
#define MINIMAX_AGENT_H


/**
 * Load minimax scores for every move
 * ----------------------------------
 * Memory allocated array score_list
 * must be passed to store the values
 */
void
minimax__load_scores ( int  *board,
                       int  *score_list,
                       int   player,
                       int   depth );


#endif