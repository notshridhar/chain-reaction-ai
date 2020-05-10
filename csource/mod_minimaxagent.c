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
static PyObject *py__load_scores (PyObject *self, PyObject *args);


/* Function Mapping Table*/
static PyMethodDef MiniMaxMethods[] = {
    {
        "load_scores",
        py__load_scores,
        METH_VARARGS,
        "Get the scores of all moves of board"
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
static PyObject *py__load_scores (PyObject *self, PyObject *args)
{
    /* Expecting arguments */
    PyObject *board;
    int       player;
    int       depth;

    /* Parse Arguments */
    if (!PyArg_ParseTuple(args, "Oii", &board, &player, &depth))
        return NULL;

    /* PyList -> C Array */
    int cboard[54];
    for (int i = 0; i < 54; ++i)
    {
        cboard[i] = (int)PyLong_AsLong(PyList_GetItem(board, i));
    }

    /* Actual Stuff */
    int score_list[54] = {0};
    minimax__load_scores(cboard, score_list, player, depth);

    /* Build Python List */
    PyObject *py_score_list = PyList_New(54);
    for (int i = 0; i < 54; ++i)
    {
        PyList_SetItem(py_score_list, i, PyLong_FromLong((long)score_list[i]));
    }
    return py_score_list;
}
