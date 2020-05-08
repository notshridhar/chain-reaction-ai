/**
 * C Extension Module for Minimax Agent
 * Exposes minimax tree search functions
*/

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>
#include "chain/minimax.h"


/* exclusive python 3 */
#if PY_MAJOR_VERSION < 3
#error "Only for Python3"
#endif


/* Function declarations */
static PyObject *py__minimizer (PyObject *self, PyObject *args);
static PyObject *py__maximizer (PyObject *self, PyObject *args);


/* Function Mapping Table*/
static PyMethodDef MiniMaxMethods[] = {
    {
        "pruned_minimizer",
        py__minimizer,
        METH_VARARGS,
        "Minimax Recursive Minimizer"
    },
    {
        "pruned_maximizer",
        py__maximizer,
        METH_VARARGS,
        "Minimax Recursive Maximizer"
    },
    {NULL, NULL, 0, NULL} // sentinel
};


/* Module Definition Structure */
static struct PyModuleDef minimaxmodule = {
    PyModuleDef_HEAD_INIT,
    "minimax_agent",  // name of module
    NULL,             // module documentation
    -1,               // module keeps state in global variable
    MiniMaxMethods
};


/* Module Initialization Function */
PyMODINIT_FUNC PyInit_minimax_agent(void)
{
    return PyModule_Create(&minimaxmodule);
}


/******************* FUNCTION DEFINITIONS *********************/
static PyObject *py__minimizer (PyObject *self, PyObject *args)
{
    /* Expecting arguments */
    PyObject *board;
    int       player;
    int       alpha;
    int       beta;
    int       depth;

    /* Parse Arguments */
    if (!PyArg_ParseTuple(args, "Oiiii", &board, &player, &alpha, &beta, &depth))
        return NULL;

    /* PyList -> C Array */
    int cboard[54];
    for (int i = 0; i < 54; ++i)
    {
        cboard[i] = (int)PyLong_AsLong(PyList_GetItem(board, i));
    }

    /* Actual Stuff */
    int score = minimax__pruned_minimizer(cboard, player, alpha, beta, depth);

    /* Build Python integer */
    return Py_BuildValue("i", score);
}

static PyObject *py__maximizer (PyObject *self, PyObject *args)
{
    /* Expecting arguments */
    PyObject *board;
    int       player;
    int       alpha;
    int       beta;
    int       depth;

    /* Parse Arguments */
    if (!PyArg_ParseTuple(args, "Oiiii", &board, &player, &alpha, &beta, &depth))
        return NULL;

    /* PyList -> C Array */
    int cboard[54];
    for (int i = 0; i < 54; ++i)
    {
        cboard[i] = (int)PyLong_AsLong(PyList_GetItem(board, i));
    }

    /* Actual Stuff */
    int score = minimax__pruned_maximizer(cboard, player, alpha, beta, depth);

    /* Build Python integer */
    return Py_BuildValue("i", score);
}
