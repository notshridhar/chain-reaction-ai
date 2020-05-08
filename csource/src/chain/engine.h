#ifndef CHAIN_ENGINE_H
#define CHAIN_ENGINE_H


/**
 * Interact with environment
 * -------------------------
 * Takes old board and stores the new state in new board
 * Returns game over status as boolean
 */
int
engine__interact ( int  *old_board,
                   int  *new_board,
                   int   move,
                   int   player );

#endif