/*
 * Copyright (c) 2017, Alexander Feldman, PARC Inc.
 * Python bindings to lgl (http://fmv.jku.at/lgl/)
 * This file is published under the same license as lingeling.
 */
#define PYLGL_URL  "https://pypi.python.org/pypi/pylgl"

#include <Python.h>

#ifdef _MSC_VER
#define NGETRUSAGE
#define inline __inline
#endif

#include "lglib.h"

#if PY_MAJOR_VERSION >= 3
#define IS_PY3K
#endif

#ifdef IS_PY3K
#define PyInt_FromLong  PyLong_FromLong
#define IS_INT(x)  (PyLong_Check(x))
#else
#define IS_INT(x)  (PyInt_Check(x) || PyLong_Check(x))
#endif

#if PY_MAJOR_VERSION == 2 && PY_MINOR_VERSION <= 5
#define PyUnicode_FromString  PyString_FromString
#endif

inline static void *py_malloc(void *mmgr, size_t bytes)
{
    return PyMem_Malloc(bytes);
}

inline static void *py_realloc(void *mmgr, void *ptr, size_t old, size_t new)
{
    return PyMem_Realloc(ptr, new);
}

inline static void py_free(void *mmgr, void *ptr, size_t bytes)
{
    PyMem_Free(ptr);
}

typedef struct {
    PyObject_HEAD
    LGL *lgl;
    signed char *mem;           /* temporary storage */
} soliterobject;

/* Add the inverse of the (current) solution to the clauses.
   This function is essentially the same as the function blocksol in app.c
   in the picosat source. */
static int blocksol(soliterobject *it)
{
    int max_idx;
    int i;
    int lit;

    max_idx = lglmaxvar(it->lgl);
    if (it->mem == NULL) {
        it->mem = PyMem_Malloc(max_idx + 1);
        if (it->mem == NULL) {
            PyErr_NoMemory();
            return -1;
        }
    }
    for (i = 1; i <= max_idx; i++) {
        it->mem[i] = (lglderef(it->lgl, i) > 0) ? 1 : -1;
    }

    for (i = 1; i <= max_idx; i++) {
        lit = (it->mem[i] < 0) ? i : -i;
        lgladd(it->lgl, lit);
        lglfreeze(it->lgl, lit);
    }

    lgladd(it->lgl, 0);

    return 0;
}

static int add_clause(LGL *lgl, PyObject *clause)
{
    PyObject *iterator;         /* each clause is an iterable of literals */
    PyObject *lit;              /* the literals are integers */
    int v;

    iterator = PyObject_GetIter(clause);
    if (iterator == NULL) {
        return -1;
    }

    while ((lit = PyIter_Next(iterator)) != NULL) {
        if (!IS_INT(lit))  {
            Py_DECREF(lit);
            Py_DECREF(iterator);
            PyErr_SetString(PyExc_TypeError, "integer expected");

            return -1;
        }
        v = PyLong_AsLong(lit);
        Py_DECREF(lit);
        if (v == 0) {
            Py_DECREF(iterator);
            PyErr_SetString(PyExc_ValueError, "non-zero integer expected");

            return -1;
        }
        lgladd(lgl, v);
        lglfreeze(lgl, v);
    }
    Py_DECREF(iterator);
    if (PyErr_Occurred()) {
        return -1;
    }
    lgladd(lgl, 0);
 
    return 0;
}

static int add_clauses(LGL *lgl, PyObject *clauses)
{
    PyObject *iterator;       /* clauses can be any iterable */
    PyObject *item;           /* each clause is an iterable of intergers */

    iterator = PyObject_GetIter(clauses);
    if (iterator == NULL) {
        return -1;
    }

    while ((item = PyIter_Next(iterator)) != NULL) {
        if (add_clause(lgl, item) < 0) {
            Py_DECREF(item);
            Py_DECREF(iterator);

            return -1;
        }
        Py_DECREF(item);
    }
    Py_DECREF(iterator);
    if (PyErr_Occurred()) {
        return -1;
    }
    return 0;
}

static LGL *setup_lgl(PyObject *args, PyObject *kwds)
{
    LGL *lgl;

    PyObject *clauses;          /* iterable of clauses */
    int vars = -1;
    int verbose = 0;
    int seed = 0;
    int simplify = 2;
    int randec = 0;
    int randecint = 809;
    int randphase = 0;
    int randphaseint = 503;
    static char *kwlist[] = { "clauses",
                              "vars",
                              "verbose",
                              "seed",
                              "simplify",
                              "randec",
                              "randecint",
                              "randphase",
                              "randphaseint",
                              NULL };

    if (!PyArg_ParseTupleAndKeywords(args,
                                     kwds,
                                     "O|iiiiiiii:(iter)solve",
                                     kwlist,
                                     &clauses,
                                     &vars,
                                     &verbose,
                                     &seed,
                                     &simplify,
                                     &randec,
                                     &randecint,
                                     &randphase,
                                     &randphaseint)) {
        return NULL;
    }

    lgl = lglminit(NULL, py_malloc, py_realloc, py_free);
    lglsetopt(lgl, "seed", seed);
    lglsetopt(lgl, "simplify", simplify);
    lglsetopt(lgl, "randec", randec);
    lglsetopt(lgl, "randecint", randecint);
    lglsetopt(lgl, "randphase", randphase);
    lglsetopt(lgl, "randphaseint", randphaseint);

    if (add_clauses(lgl, clauses) < 0) {
        return NULL;
    }
    
    return lgl;
}

static void destroy_lgl(LGL *lgl)
{
    lglrelease(lgl);
}

static PyObject* get_solution(LGL *lgl)
{
    PyObject *list;
    int max_idx;
    int i;
    int v;

    max_idx = lglmaxvar(lgl);
    list = PyList_New((Py_ssize_t)max_idx);
    if (list == NULL) {
        return NULL;
    }
    for (i = 1; i <= max_idx; i++) {
        v = lglderef(lgl, i);
        assert(v == -1 || v == 1);
        if (PyList_SetItem(list,
                           (Py_ssize_t)(i - 1),
                           PyInt_FromLong((long) (v * i))) < 0) {
            Py_DECREF(list);
            return NULL;
        }
    }
    return list;
}

static PyObject *solve(PyObject *self, PyObject *args, PyObject *kwds)
{
    LGL *lgl;
    PyObject *result = NULL;
    int rc;

    lgl = setup_lgl(args, kwds);
    if (lgl == NULL) {
        return NULL;
    }

    Py_BEGIN_ALLOW_THREADS      /* release GIL */
    rc = lglsat(lgl);
    Py_END_ALLOW_THREADS

    switch (rc) {
        case LGL_SATISFIABLE:
            result = get_solution(lgl);
            break;
        case LGL_UNSATISFIABLE:
            result = PyUnicode_FromString("UNSAT");
            break;
        case LGL_UNKNOWN:
            result = PyUnicode_FromString("UNKNOWN");
            break;
        default:
            PyErr_Format(PyExc_SystemError, "picosat return value: %d", rc);
    }

    destroy_lgl(lgl);

    return result;
}

PyDoc_STRVAR(solve_doc,
"solve(clauses [, kwargs]) -> list\n\
\n\
Solve the SAT problem for the clauses, and return a solution as a\n\
list of integers, or one of the strings \"UNSAT\", \"UNKNOWN\".\n\
Please see " PYLGL_URL " for more details.");

static PyTypeObject SolIter_Type;

#define SolIter_Check(op) PyObject_TypeCheck(op, &SolIter_Type)

static PyObject *itersolve(PyObject *self, PyObject *args, PyObject *kwds)
{
    soliterobject *it;          /* iterator to be returned */

    it = PyObject_GC_New(soliterobject, &SolIter_Type);
    if (it == NULL) {
        return NULL;
    }

    it->lgl = setup_lgl(args, kwds);
    if (it->lgl == NULL) {
        return NULL;
    }

    it->mem = NULL;
    PyObject_GC_Track(it);
    return (PyObject *)it;
}

PyDoc_STRVAR(itersolve_doc,
"itersolve(clauses [, kwargs]) -> interator\n\
\n\
Solve the SAT problem for the clauses, and return an iterator over\n\
the solutions (which are lists of integers).\n\
Please see " PYLGL_URL " for more details.");

static PyObject* soliter_next(soliterobject *it)
{
    PyObject *result = NULL;
    int rc;

    assert(SolIter_Check(it));

    Py_BEGIN_ALLOW_THREADS      /* release GIL */
    rc = lglsat(it->lgl);
    Py_END_ALLOW_THREADS

    switch (rc) {
        case LGL_SATISFIABLE:
            result = get_solution(it->lgl);
            if (result == NULL) {
                PyErr_SetString(PyExc_SystemError, "failed to create list");
                return NULL;
            }
            /* add inverse solution to the clauses, for next interation */
            if (blocksol(it) < 0) {
                return NULL;
            }
        break;
        case LGL_UNSATISFIABLE:
        case LGL_UNKNOWN:
            /* no more solutions -- stop iteration */
            break;
        default:
            PyErr_Format(PyExc_SystemError, "lingeling return value: %d", rc);
    }
    return result;
}

static void soliter_dealloc(soliterobject *it)
{
    PyObject_GC_UnTrack(it);
    if (it->mem) {
        PyMem_Free(it->mem);
    }

    destroy_lgl(it->lgl);

    PyObject_GC_Del(it);
}

static int soliter_traverse(soliterobject *it, visitproc visit, void *arg)
{
    return 0;
}

static PyTypeObject SolIter_Type = {
#ifdef IS_PY3K
    PyVarObject_HEAD_INIT(NULL, 0)
#else
    PyObject_HEAD_INIT(NULL)
    0,                                        /* ob_size */
#endif
    "soliterator",                            /* tp_name */
    sizeof(soliterobject),                    /* tp_basicsize */
    0,                                        /* tp_itemsize */
    /* methods */
    (destructor)soliter_dealloc,              /* tp_dealloc */
    0,                                        /* tp_print */
    0,                                        /* tp_getattr */
    0,                                        /* tp_setattr */
    0,                                        /* tp_compare */
    0,                                        /* tp_repr */
    0,                                        /* tp_as_number */
    0,                                        /* tp_as_sequence */
    0,                                        /* tp_as_mapping */
    0,                                        /* tp_hash */
    0,                                        /* tp_call */
    0,                                        /* tp_str */
    PyObject_GenericGetAttr,                  /* tp_getattro */
    0,                                        /* tp_setattro */
    0,                                        /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC,  /* tp_flags */
    0,                                        /* tp_doc */
    (traverseproc)soliter_traverse,           /* tp_traverse */
    0,                                        /* tp_clear */
    0,                                        /* tp_richcompare */
    0,                                        /* tp_weaklistoffset */
    PyObject_SelfIter,                        /* tp_iter */
    (iternextfunc)soliter_next,               /* tp_iternext */
    0,                                        /* tp_methods */
};

/* Method definitions */

/* declaration of methods supported by this module */
static PyMethodDef module_functions[] = {
    {"solve",     (PyCFunction)solve,     METH_VARARGS | METH_KEYWORDS, solve_doc},
    {"itersolve", (PyCFunction)itersolve, METH_VARARGS | METH_KEYWORDS, itersolve_doc},
    {NULL,        NULL}  /* sentinel */
};

PyDoc_STRVAR(module_doc, "\
pylgl: bindings to lgl\n\
============================\n\n\
There are two functions in this module, solve and itersolve.\n\
Please see " PYLGL_URL " for more details.");

/* initialization routine for the shared libary */
#ifdef IS_PY3K
static PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT, "pylgl", module_doc, -1, module_functions,
};

PyMODINIT_FUNC PyInit_pylgl(void)
#else
PyMODINIT_FUNC initpylgl(void)
#endif
{
    PyObject *m;

#ifdef IS_PY3K
    if (PyType_Ready(&SolIter_Type) < 0) {
        return NULL;
    }

    m = PyModule_Create(&moduledef);
    if (m == NULL) {
        return NULL;
    }
#else
    if (PyType_Ready(&SolIter_Type) < 0) {
        return;
    }

    m = Py_InitModule3("pylgl", module_functions, module_doc);
    if (m == NULL) {
        return;
    }
#endif

#ifdef PYLGL_VERSION
    PyModule_AddObject(m, "__version__", PyUnicode_FromString(PYLGL_VERSION));
#endif
    
#ifdef IS_PY3K
    return m;
#endif
}
