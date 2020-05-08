#include <stdlib.h>
#include "chain/cqueue.h"

CQueue *cqueue__create(int capacity)
{
    CQueue *nq = malloc(sizeof(CQueue));
    nq->head = 0;
    nq->tail = 0;
    nq->size = capacity;
    nq->arr = malloc(capacity * sizeof(int));
    return nq;
}

void cqueue__destory(CQueue *self)
{
    free(self->arr);
    free(self);
    self->arr = NULL;
}

/* Returns true if success, false if failed */
char cqueue__enqueue(CQueue *self, int element)
{
    self->arr[self->tail] = element;
    self->tail = (self->tail + 1) % self->size;
    return (self->tail == self->head);
}

/**
 * Warning: No size checking, can retrieve garbage data
 * Check if queue is empty before retrieving elements
 */
int cqueue__dequeue(CQueue *self)
{
    int element = self->arr[self->head];
    self->head = (self->head + 1) % self->size;
    return element;
}

char cqueue__isempty(CQueue *self)
{
    return (self->tail == self->head);
}