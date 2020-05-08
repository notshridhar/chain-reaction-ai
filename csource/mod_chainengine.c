/**
 * C Extension Module for Chain Reaction Engine
 * Exposes environment interaction functions
*/

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>
#include "chain/engine.h"


/* exclusive python 3 */
#if PY_MAJOR_VERSION < 3
#error "Only for Python3"
#endif


/* Function declarations */
static PyObject *py_engine__interact (PyObject *self, PyObject *args);


/* Function Mapping Table*/
static PyMethodDef ChainEngineMethods[] = {
    {
        "interact_inplace",
        py_engine__interact,
        METH_VARARGS,
        "Interact with Chain Reaction Game Environment"
    },
    {NULL, NULL, 0, NULL} // sentinel
};


/* Module Definition Structure */
static struct PyModuleDef chainenginemodule = {
    PyModuleDef_HEAD_INIT,
    "chain_engine",  // name of module
    NULL,            // module documentation
    -1,              // module keeps state in global variable
    ChainEngineMethods
};


/* Module Initialization Function */
PyMODINIT_FUNC PyInit_chain_engine(void)
{
    return PyModule_Create(&chainenginemodule);
}


/********************* FUNCTION DEFINITION ************************/
static PyObject *py_engine__interact(PyObject *self, PyObject *args)
{
    /* Expecting arguments */
    PyObject *board;
    int       move;
    int       player;

    /* Parse Arguments */
    if (!PyArg_ParseTuple(args, "Oii", &board, &move, &player))
        return NULL;

    /* PyList -> C Array */
    int cboard[54];
    for (int i = 0; i < 54; ++i)
    {
        cboard[i] = (int)PyLong_AsLong(PyList_GetItem(board, i));
    }
 
    /* Actual Stuff */
    int nboard[54];
    int game_over = engine__interact(cboard, nboard, move, player);

    /* C Array -> PyList */
    for (int i = 0; i < 54; ++i)
    {
        PyList_SetItem(board, i, PyLong_FromLong((long)nboard[i]));
    }

    return Py_BuildValue("i", game_over);
}