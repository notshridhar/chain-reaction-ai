/**
 * Circular Queue of Integers
 * --------------------------
 * FIFO Data Structure
 */

#ifndef CIRC_QUEUE_H
#define CIRC_QUEUE_H


typedef struct
{
    int head;
    int tail;
    int size;
    int *arr;
} CQueue;


/* CQueue Methods */
CQueue   *cqueue__create  (int capacity);
void      cqueue__destory (CQueue *self);
char      cqueue__enqueue (CQueue *self, int element);
int       cqueue__dequeue (CQueue *self);
char      cqueue__isempty (CQueue *self);


#endif