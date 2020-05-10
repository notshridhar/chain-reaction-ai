#include "chain/cqueue.h"
#include "chain/engine.h"


/* Critical Mass Lookup Table */
static const int NTABLE [9 * 6] = {
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


/* Interact with environment */
int
engine__interact ( int  *old_board,
                   int  *new_board,
                   int   move,
                   int   player )
{
    int game_over = 0;
    int psign     = player ? -1 : 1;
    int t_frn     = 0;
    int t_enm     = 0;

    /* queue acts as reactions sequence */
    CQueue *work = cqueue__create(100);
    cqueue__enqueue(work, move);

    /* count territories while copying whole board */
    for (int i = 0; i < 54; ++i)
    {
        new_board[i] = old_board[i];         // copy
        if      (new_board[i] > 0)  ++t_frn; // positive
        else if (new_board[i] < 0)  ++t_enm; // negative
    }

    /* swap enemy and friend counts if player is 1 */
    if (player)
    {
        int temp = t_frn;
        t_frn = t_enm;
        t_enm = temp;
    }

    /* stop if game over or the queue is empty */
    while ((!game_over) && (!cqueue__isempty(work)))
    {
        /* get next index in queue */
        move = cqueue__dequeue(work);

        /* update territory counts and game over */
        t_frn += 1;
        t_enm -= (new_board[move] * psign < 0);
        game_over = ((t_enm + t_frn > 2) && (t_enm * t_frn == 0));
    
        /* update orb count */
        int cell = new_board[move];
        int absl = (cell > 0) ? cell : -cell;
        new_board[move] = ((absl + 1) % NTABLE[move]) * psign;

        /* add neighbors to queue if exploded */
        if (absl + 1 == NTABLE[move])
        {
            int i_y = move / 6;
            int i_x = move % 6;

            if (i_y > 0)  { cqueue__enqueue(work, move - 6); }
            if (i_y < 8)  { cqueue__enqueue(work, move + 6); }
            if (i_x > 0)  { cqueue__enqueue(work, move - 1); }
            if (i_x < 5)  { cqueue__enqueue(work, move + 1); }
        }    
    }

    /* cleanup */
    cqueue__destory(work);
    return game_over;
}
