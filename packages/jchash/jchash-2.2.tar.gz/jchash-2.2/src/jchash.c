#include <Python.h>
#include <stdint.h>

// jchash doc string
PyDoc_STRVAR(Py_Jchash_doc, "Jump Consistent Hash, a fast, minimal memory, \
    consistent hash algorithm by John Lamping, Eric Veach, Google.");

static int64_t jchash(uint64_t key, int32_t num_buckets)
{
    int64_t b = -1, j = 0;
    while (j < num_buckets) {
        b = j;
        key = key * 2862933555777941757ULL + 1;
        j = (b + 1) * ((double) (1LL << 31) / (double) ((key >> 33) + 1));
    }
    return b;
}

static uint64_t string_hash(char *s)
{
    uint64_t seed = 131;
    uint64_t hash = 0;

    while (*s) {
        hash = hash * seed + (*s++);
    }

    return (hash & 0x7FFFFFFFFFFFFFFF);
}

static PyObject *
jchash_jchash(PyObject *self, PyObject *args)
{
    PyObject *pykey = NULL;
    uint64_t key = 0;
    int32_t num_buckets = 0;

    if (!PyArg_ParseTuple(args, "Oi", &pykey, &num_buckets)) {
        return NULL;
    }

    // Check pykey is int or string
    if (PyLong_Check(pykey)) {
        key = PyLong_AsUnsignedLongLong(pykey);

        // Occurred negative, raised Overflow Error
        if (PyErr_Occurred()) {
            return NULL;
        }
    } else if (PyBytes_Check(pykey)) {
        char *s = PyBytes_AsString(pykey);
        key = string_hash(s);
    } else if (PyFloat_Check(pykey)) {
        PyErr_SetString(PyExc_TypeError, "Key should be int or bytes, not float");
        return NULL;
    } else if (PyUnicode_Check(pykey)) {
        PyErr_SetString(PyExc_TypeError, "Key should be int or bytes, not string");
        return NULL;
    } else {
        PyErr_SetString(PyExc_TypeError, "Key should be int or bytes");
        return NULL;
    }

    return PyLong_FromLongLong(jchash(key, num_buckets));
}

static PyMethodDef jchash_methods[] = {
    {"jchash", jchash_jchash, METH_VARARGS, "jchash."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef jchash_module = {
    PyModuleDef_HEAD_INIT,
    XSTR(JCHASH_MODULE_NAME),
    Py_Jchash_doc,
    -1,
    jchash_methods
};

PyMODINIT_FUNC
PyInit_jchash(void)
{
    PyObject *m;

    m = PyModule_Create(&jchash_module);
    if (m == NULL) {
        return NULL;
    }

    if (PyModule_AddStringConstant(m, "__version__", XSTR(PACKAGE_VERSION))) {
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
