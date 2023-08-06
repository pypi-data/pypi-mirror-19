/*
# This file is part of PyORTHPOL.
#
# PyORTHPOL is free software: you can redistribute it and/or modify
# it under the terms of the LGNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyORTHPOL is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# LGNU Lesser General Public License for more details.
#
# You should have received a copy of the LGNU Lesser General Public License
# along with PyORTHPOL.  If not, see <http://www.gnu.org/licenses/>.
#
# DTU UQ Library
# Copyright (C) 2014-2015 The Technical University of Denmark
# Scientific Computing Section
# Department of Applied Mathematics and Computer Science
#
# Copyright (C) 2015-2016 Massachusetts Institute of Technology
# Uncertainty Quantification group
# Department of Aeronautics and Astronautics
#
# Author: Daniele Bigoni
*/

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

#include <Python.h>
#include <numpy/ndarrayobject.h>
#include <numpy/ndarraytypes.h>
#include <math.h>

#include <ORTHPOLxx/ORTHPOLPP.hpp>

#if PY_MAJOR_VERSION >= 3
    #define MOD_INIT(name) PyMODINIT_FUNC PyInit_##name(void)
#else
    #define MOD_INIT(name) PyMODINIT_FUNC init##name(void)
#endif

using namespace std;

static PyObject *ORTHPOLError;
static PyObject *polymodError;

/* .... C vector utility functions ..................*/
PyArrayObject *pyvector(PyObject *objin);
double *pyvector_to_Carrayptrs(PyArrayObject *arrayin);
int  not_doublevector(PyArrayObject *vec);

/* .... C matrix utility functions ..................*/
PyArrayObject *pymatrix(PyObject *objin);
double **pymatrix_to_Carrayptrs(PyArrayObject *arrayin);
double **ptrvector(long n);
void free_Carrayptrs(double **v);
int  not_doublematrix(PyArrayObject *mat);

/* .... C 2D int array utility functions ..................*/
PyArrayObject *pyint2Darray(PyObject *objin);
int **pyint2Darray_to_Carrayptrs(PyArrayObject *arrayin);
int **ptrintvector(long n);
void free_Cint2Darrayptrs(int **v);
int  not_int2Darray(PyArrayObject *mat);


/* ORTHPOL functions declaration */
static PyObject* Py_r1mach (PyObject *self, PyObject *args);
static PyObject* Py_d1mach (PyObject *self, PyObject *args);
static PyObject* Py_dcheb  (PyObject *self, PyObject *args);
static PyObject* Py_dchri  (PyObject *self, PyObject *args);
static PyObject* Py_dgauss (PyObject *self, PyObject *args);
static PyObject* Py_dgchri (PyObject *self, PyObject *args);
static PyObject* Py_dlancz (PyObject *self, PyObject *args);
static PyObject* Py_dlob   (PyObject *self, PyObject *args);
static PyObject* Py_dmcheb (PyObject *self, PyObject *args);
static PyObject* Py_dmcdis (PyObject *self, PyObject *args);
static PyObject* Py_dradau (PyObject *self, PyObject *args);
static PyObject* Py_drecur (PyObject *self, PyObject *args);
static PyObject* Py_dsti   (PyObject *self, PyObject *args);
/* polymod functions declaration */
static PyObject* Py_polyeval (PyObject *self, PyObject *args);
static PyObject* Py_monomials (PyObject *self, PyObject *args);
static PyObject* Py_numeric_gamma (PyObject *self, PyObject *args);
static PyObject* Py_vandermonde (PyObject *self, PyObject *args);

/* PyORTHPOL set callback functions declarations */
static PyObject* set_dquad_callback(PyObject *self, PyObject *args);
static PyObject* set_dwf_callback(PyObject *self, PyObject *args);

/* ORTHPOL Python callback functions declarations */
static PyObject *dquad_callback = NULL;
static PyObject *dwf_callback = NULL;

/* C++ callback functions declaration */
void dquad_callback_func(int& n, double* x, double* w, int& i, int& ierr);
double dwf_callback_func(double& x, int& i);

/* PyORTHPOL list of methods definition */
static PyMethodDef ORTHPOLMethods[] = {
  {"r1mach", Py_r1mach, METH_VARARGS, "Retrive single machine precision."},
  {"d1mach", Py_d1mach, METH_VARARGS, "Retrive double machine precision."},
  {"dcheb",  Py_dcheb,  METH_VARARGS, "Use the modified Chebyshev algorithm to compute moment-related coefficients."},
  {"dchri",  Py_dchri,  METH_VARARGS, "Applies the Nonlinear recurrence algorithm for modified measures."},
  {"dgauss", Py_dgauss, METH_VARARGS, "Computes the Gauss quadrature nodes and weights using the recursion coefficients alpha and beta."},
  {"dgchri", Py_dgchri, METH_VARARGS, "Applies the Modified Chebyshev algorithm for modified measures."},
  {"dlancz", Py_dlancz, METH_VARARGS, "Applies the Orthogonal Reduction method."},
  {"dlob",   Py_dlob,   METH_VARARGS, "Computes the Gauss-Lobatto quadrature nodes and weights using the recursion coefficients alpha and beta."},
  {"dmcheb", Py_dmcheb, METH_VARARGS, "Discretized Modified Chebyshev Algorithm."},
  {"dmcdis", Py_dmcdis, METH_VARARGS, "Multiple-Component discretization procedure."},
  {"dradau", Py_dradau,  METH_VARARGS, "Computes the Gauss-Radau quadrature nodes and weights using the recursion coefficients alpha and beta."},
  {"drecur", Py_drecur, METH_VARARGS, "Retrive recursion coefficients for standard polynomial classes."},
  {"dsti",   Py_dsti,   METH_VARARGS, "Applies the Stieltjes procedure."},
  {"set_dquad_callback", set_dquad_callback, METH_VARARGS, "Set the dquad callback function"},
  {"set_dwf_callback", set_dwf_callback, METH_VARARGS, "Set the dwf callback function"},
  {"polyeval", Py_polyeval, METH_VARARGS, "Given a set of points and the N+1 recursion coefficients, evaluate the polynomial of order N, normalized."},
  {"monomials", Py_monomials, METH_VARARGS, "Given the N+1 recursion coefficients, evaluate the monomials coefficients."},
  {"numeric_gamma", Py_numeric_gamma, METH_VARARGS, "Compute the normalization constant for the N-th polynomial."},
  {"vandermonde", Py_vandermonde, METH_VARARGS, "Given a set of points and the N+1 recursion coefficients, evaluate the vandermonde matrix of order N, normalized."},
  {NULL, NULL, 0, NULL}        /* Sentinel */
};

/* #### Vector Utility functions ######################### */

/* ==== Make a Python Array Obj. from a PyObject, ================
     generates a double vector w/ contiguous memory which may be a new allocation if
     the original was not a double type or contiguous 
  !! Must DECREF the object returned from this routine unless it is returned to the
     caller of this routines caller using return PyArray_Return(obj) or
     PyArray_BuildValue with the "N" construct   !!!
*/
PyArrayObject *pyvector(PyObject *objin)  {
	return (PyArrayObject *) PyArray_ContiguousFromObject(objin,
		NPY_DOUBLE, 1,1);
}
/* ==== Create 1D Carray from PyArray ======================
    Assumes PyArray is contiguous in memory.             */
double *pyvector_to_Carrayptrs(PyArrayObject *arrayin)  {
  return (double *) PyArray_DATA(arrayin);  /* pointer to arrayin data as double */
}
/* ==== Check that PyArrayObject is a double (Float) type and a vector ==============
    return 1 if an error and raise exception */ 
int  not_doublevector(PyArrayObject *vec)  {
  if (PyArray_DESCR(vec)->type_num != NPY_DOUBLE || PyArray_NDIM(vec) != 1)  {
    PyErr_SetString(PyExc_ValueError,
                    "In not_doublevector: array must be of type Float and 1 dimensional (n).");
    return 1;  }
  return 0;
}

/* #### Matrix Utility functions ######################### */

/* ==== Make a Python Array Obj. from a PyObject, ================
     generates a double matrix w/ contiguous memory which may be a new allocation if
     the original was not a double type or contiguous 
  !! Must DECREF the object returned from this routine unless it is returned to the
     caller of this routines caller using return PyArray_Return(obj) or
     PyArray_BuildValue with the "N" construct   !!!
*/
PyArrayObject *pymatrix(PyObject *objin)  {
	return (PyArrayObject *) PyArray_ContiguousFromObject(objin,
		NPY_DOUBLE, 2,2);
}
/* ==== Create Carray from PyArray ======================
    Assumes PyArray is contiguous in memory.
    Memory is allocated!                                    */
double **pymatrix_to_Carrayptrs(PyArrayObject *arrayin)  {
	double **c, *a;
	int i,n,m;
	
	n=PyArray_DIMS(arrayin)[0];
	m=PyArray_DIMS(arrayin)[1];
	c=ptrvector(n);
	a=(double *) PyArray_DATA(arrayin);  /* pointer to arrayin data as double */
	for ( i=0; i<n; i++)  {
		c[i]=a+i*m;  }
	return c;
}
/* ==== Allocate a double *vector (vec of pointers) ======================
    Memory is Allocated!  See void free_Carray(double ** )                  */
double **ptrvector(long n)  {
	double **v;
	v=(double **)malloc((size_t) (n*sizeof(double)));
	if (!v)   {
		printf("In **ptrvector. Allocation of memory for double array failed.");
		exit(0);  }
	return v;
}
/* ==== Free a double *vector (vec of pointers) ========================== */ 
void free_Carrayptrs(double **v)  {
	free((char*) v);
}
/* ==== Check that PyArrayObject is a double (Float) type and a matrix ==============
    return 1 if an error and raise exception */ 
int  not_doublematrix(PyArrayObject *mat)  {
  if (PyArray_DESCR(mat)->type_num != NPY_DOUBLE || PyArray_NDIM(mat) != 2)  {
    PyErr_SetString(PyExc_ValueError,
                    "In not_doublematrix: array must be of type Float and 2 dimensional (n x m).");
    return 1;  }
  return 0;
}

/* #### Integer Array Utility functions ######################### */

/* ==== Make a Python int Array Obj. from a PyObject, ================
     generates a 2D integer array w/ contiguous memory which may be a new allocation if
     the original was not an integer type or contiguous 
  !! Must DECREF the object returned from this routine unless it is returned to the
     caller of this routines caller using return PyArray_Return(obj) or
     PyArray_BuildValue with the "N" construct   !!!
*/
PyArrayObject *pyint2Darray(PyObject *objin)  {
	return (PyArrayObject *) PyArray_ContiguousFromObject(objin,
		NPY_LONG, 2,2);
}
/* ==== Create integer 2D Carray from PyArray ======================
    Assumes PyArray is contiguous in memory.
    Memory is allocated!                                    */
int **pyint2Darray_to_Carrayptrs(PyArrayObject *arrayin)  {
	int **c, *a;
	int i,n,m;
	
	n=PyArray_DIMS(arrayin)[0];
	m=PyArray_DIMS(arrayin)[1];
	c=ptrintvector(n);
	a=(int *) PyArray_DATA(arrayin);  /* pointer to arrayin data as int */
	for ( i=0; i<n; i++)  {
		c[i]=a+i*m;  }
	return c;
}
/* ==== Allocate a a *int (vec of pointers) ======================
    Memory is Allocated!  See void free_Carray(int ** )                  */
int **ptrintvector(long n)  {
	int **v;
	v=(int **)malloc((size_t) (n*sizeof(int)));
	if (!v)   {
		printf("In **ptrintvector. Allocation of memory for int array failed.");
		exit(0);  }
	return v;
}
/* ==== Free an int *vector (vec of pointers) ========================== */ 
void free_Cint2Darrayptrs(int **v)  {
	free((char*) v);
}
/* ==== Check that PyArrayObject is an int (integer) type and a 2D array ==============
    return 1 if an error and raise exception
    Note:  Use NY_LONG for NumPy integer array, not NP_INT      */ 
int  not_int2Darray(PyArrayObject *mat)  {
  if (PyArray_DESCR(mat)->type_num != NPY_LONG || PyArray_NDIM(mat) != 2)  {
    PyErr_SetString(PyExc_ValueError,
                    "In not_int2Darray: array must be of type int and 2 dimensional (n x m).");
    return 1;  }
  return 0;
}


/* Init Package function definition */
MOD_INIT(orthpol)
{
    PyObject *m;

#if PY_MAJOR_VERSION >= 3
    static struct PyModuleDef moduledef = {
      PyModuleDef_HEAD_INIT,
      "orthpol",           /* m_name */
      "Python porting of ORTHPOL",  /* m_doc */
      -1,                  /* m_size */
      ORTHPOLMethods,      /* m_methods */
      NULL,                /* m_reload */
      NULL,                /* m_traverse */
      NULL,                /* m_clear */
      NULL,                /* m_free */
    };
#endif
    
#if PY_MAJOR_VERSION >= 3
    m = PyModule_Create(&moduledef);
    if (m == NULL) return NULL;
#else
    m = Py_InitModule3("orthpol", ORTHPOLMethods, "Python porting of ORTHPOL");
    if (m == NULL) return;
#endif

    import_array();

    ORTHPOLError = PyErr_NewException(const_cast<char *>("orthpol.error"), NULL, NULL);
    Py_INCREF(ORTHPOLError);
    PyModule_AddObject(m, "error", ORTHPOLError);

    polymodError = PyErr_NewException(const_cast<char *>("polymod.error"), NULL, NULL);
    Py_INCREF(polymodError);
    PyModule_AddObject(m, "error", polymodError);

    // Set callbacks functions for orthpol package
    orthpol::set_dquad_callback(dquad_callback_func);
    orthpol::set_dwf_callback(dwf_callback_func);

#if PY_MAJOR_VERSION >= 3
    return m;
#endif
}

/* ORTHPOL functions definitions */
static PyObject *
Py_r1mach(PyObject *self, PyObject *args)
{
  int I;
  float result;

  if (!PyArg_ParseTuple(args, "i", &I))
    return NULL;
    
  result = orthpol::r1mach(I);
  return Py_BuildValue("f",result);
}

static PyObject *
Py_d1mach(PyObject *self, PyObject *args)
{
  int I;
  double result;

  if (!PyArg_ParseTuple(args, "i", &I))
    return NULL;
    
  result = orthpol::d1mach(I);
  return Py_BuildValue("d",result);
}

static PyObject *
Py_dcheb(PyObject *self, PyObject *args)
{
  /* VARIABLES */
  // INPUT
  int n;
  PyArrayObject *py_a, *py_b, *py_fnu;
  double *a, *b, *fnu;
  // OUTPUT
  PyArrayObject *py_alpha, *py_beta, *py_s;
  double *alpha, *beta, *s;
  int ierr;
  // INTERNAL
  double *s0, *s1, *s2;
  
  if (!PyArg_ParseTuple(args, "iO!O!O!", &n, &PyArray_Type, &py_a, &PyArray_Type, &py_b, &PyArray_Type, &py_fnu))
    return NULL;
  if (NULL == py_a) return NULL;
  if (NULL == py_b) return NULL;
  if (NULL == py_fnu) return NULL;

  // Check double type
  if (not_doublevector(py_a)) return NULL;
  if (not_doublevector(py_b)) return NULL;
  if (not_doublevector(py_fnu)) return NULL;

  int nd = 1;
  npy_intp *dims = new npy_intp[2];
  dims[0] = n;
  // PyArray to C
  a = pyvector_to_Carrayptrs(py_a);
  b = pyvector_to_Carrayptrs(py_b);
  fnu = pyvector_to_Carrayptrs(py_fnu);
  // Allocate output variables
  py_alpha = (PyArrayObject*) PyArray_SimpleNew(nd, dims, NPY_DOUBLE);
  py_beta = (PyArrayObject*) PyArray_SimpleNew(nd, dims, NPY_DOUBLE);
  py_s = (PyArrayObject*) PyArray_SimpleNew(nd, dims, NPY_DOUBLE);
  alpha = pyvector_to_Carrayptrs(py_alpha);
  beta = pyvector_to_Carrayptrs(py_beta);
  s = pyvector_to_Carrayptrs(py_s);
  // Allocate internal variables
  s0 = new double[n];
  s1 = new double[n];
  s2 = new double[n];
  
  // Call ORTHPOL library function
  orthpol::dcheb(n, a, b, fnu, alpha, beta, s, ierr, s0, s1, s2);

  // Free memory
  delete [] dims;
  delete [] s0;
  delete [] s1;
  delete [] s2;

  return Py_BuildValue("NNNi", py_alpha, py_beta, py_s, ierr);
}

static PyObject *
Py_dchri(PyObject *self, PyObject *args)
{
  /* VARIABLES */
  // INPUT
  int n;
  int iopt;
  PyArrayObject *py_a, *py_b;
  double *a, *b;
  double x, y, hr, hi;
  // OUTPUT
  PyArrayObject *py_alpha, *py_beta;
  double *alpha, *beta;
  int ierr;
  
  if (!PyArg_ParseTuple(args, "iiO!O!dddd", &n, &iopt, &PyArray_Type, &py_a, &PyArray_Type, &py_b, &x, &y, &hr, &hi))
    return NULL;
  if (NULL == py_a) return NULL;
  if (NULL == py_b) return NULL;

  // Check double type
  if (not_doublevector(py_a)) return NULL;
  if (not_doublevector(py_b)) return NULL;

  int nd = 1;
  npy_intp *dims = new npy_intp[2];
  dims[0] = n;
  // PyArray to C
  a = pyvector_to_Carrayptrs(py_a);
  b = pyvector_to_Carrayptrs(py_b);
  // Allocate output variables
  py_alpha = (PyArrayObject*) PyArray_SimpleNew(nd, dims, NPY_DOUBLE);
  py_beta = (PyArrayObject*) PyArray_SimpleNew(nd, dims, NPY_DOUBLE);
  alpha = pyvector_to_Carrayptrs(py_alpha);
  beta = pyvector_to_Carrayptrs(py_beta);
  
  // Call ORTHPOL library function
  orthpol::dchri(n, iopt, a, b, x, y, hr, hi, alpha, beta, ierr);

  // Free memory
  delete [] dims;

  return Py_BuildValue("NNi", py_alpha, py_beta, ierr);
}

static PyObject *
Py_dgauss(PyObject *self, PyObject *args)
{
  /* VARIABLES */
  // INPUT
  int n;
  PyArrayObject *py_a, *py_b;
  double *a, *b;
  // OUTPUT
  PyArrayObject *py_zero, *py_weight;
  double *zero, *weight;
  int ierr;
  // INTERNAL
  double *e;
  
  if (!PyArg_ParseTuple(args, "iO!O!", &n, &PyArray_Type, &py_a, &PyArray_Type, &py_b))
    return NULL;
  if (NULL == py_a) return NULL;
  if (NULL == py_b) return NULL;

  // Check double type
  if (not_doublevector(py_a)) return NULL;
  if (not_doublevector(py_b)) return NULL;

  int nd = 1;
  npy_intp *dims = new npy_intp[2];
  dims[0] = n;
  // PyArray to C
  if ((PyArray_DIMS(py_a)[0] != dims[0]) or (PyArray_DIMS(py_b)[0] != dims[0])){
    PyErr_SetString(polymodError, "a and b must contain n coefficients.");
    return Py_BuildValue("iii", 0, 0, 1);
  }
  a = pyvector_to_Carrayptrs(py_a);
  b = pyvector_to_Carrayptrs(py_b);
  // Allocate output variables
  py_zero = (PyArrayObject*) PyArray_SimpleNew(nd, dims, NPY_DOUBLE);
  py_weight = (PyArrayObject*) PyArray_SimpleNew(nd, dims, NPY_DOUBLE);
  zero = pyvector_to_Carrayptrs(py_zero);
  weight = pyvector_to_Carrayptrs(py_weight);
  // Allocate internal variables
  e = new double[n];
  
  // Call ORTHPOL library function
  orthpol::dgauss(n, a, b, zero, weight, ierr, e);

  // Free space
  delete [] e;
  delete [] dims;

  return Py_BuildValue("NNi", py_zero, py_weight, ierr);
}

static PyObject *
Py_dgchri(PyObject *self, PyObject *args)
{
  /* VARIABLES */
  // INPUT
  int n;
  int iopt;
  int nu0;
  int numax;
  double eps;
  PyArrayObject *py_a, *py_b;
  double *a, *b;
  double x, y;
  // OUTPUT
  PyArrayObject *py_alpha, *py_beta;
  double *alpha, *beta;
  int nu;
  int ierr;
  int ierrc;
  // INTERNAL
  double *fnu;
  double *s;
  double *s0;
  double *s1;
  double *s2;
  
  if (!PyArg_ParseTuple(args, "iiiidO!O!dd", &n, &iopt, &nu0, &numax, &eps, &PyArray_Type, &py_a, &PyArray_Type, &py_b, &x, &y))
    return NULL;
  if (NULL == py_a) return NULL;
  if (NULL == py_b) return NULL;

  // Check double type
  if (not_doublevector(py_a)) return NULL;
  if (not_doublevector(py_b)) return NULL;

  int nd = 1;
  npy_intp *dims = new npy_intp[2];
  dims[0] = n;
  // PyArray to C
  a = pyvector_to_Carrayptrs(py_a);
  b = pyvector_to_Carrayptrs(py_b);
  // Allocate output variables
  py_alpha = (PyArrayObject*) PyArray_SimpleNew(nd, dims, NPY_DOUBLE);
  py_beta = (PyArrayObject*) PyArray_SimpleNew(nd, dims, NPY_DOUBLE);
  alpha = pyvector_to_Carrayptrs(py_alpha);
  beta = pyvector_to_Carrayptrs(py_beta);
  // Allocate internal variables
  fnu = new double[2*n];
  s = new double[n];
  s0 = new double[2*n];
  s1 = new double[2*n];
  s2 = new double[2*n];
  
  // Call ORTHPOL library function
  orthpol::dgchri(n, iopt, nu0, numax, eps, a, b, x, y, alpha, beta, nu, ierr, ierrc, fnu, s, s0, s1, s2);

  // Free memory
  delete [] dims;
  delete [] fnu;
  delete [] s;
  delete [] s0;
  delete [] s1;
  delete [] s2;

  return Py_BuildValue("NNiii", py_alpha, py_beta, nu, ierr, ierrc);
}

static PyObject *
Py_dlancz(PyObject *self, PyObject *args)
{
  /* VARIABLES */
  // INPUT
  int n;
  int ncap;
  PyArrayObject *py_x, *py_y;
  double *x, *y;
  // OUTPUT
  PyArrayObject *py_alpha, *py_beta;
  double *alpha, *beta;
  int ierr;
  // INTERNAL
  double *p0;
  double *p1;
  
  if (!PyArg_ParseTuple(args, "iiO!O!", &n, &ncap, &PyArray_Type, &py_x, &PyArray_Type, &py_y))
    return NULL;
  if (NULL == py_x) return NULL;
  if (NULL == py_y) return NULL;

  // Check double type
  if (not_doublevector(py_x)) return NULL;
  if (not_doublevector(py_y)) return NULL;

  int nd = 1;
  npy_intp *dims = new npy_intp[2];
  dims[0] = n;
  // PyArray to C
  x = pyvector_to_Carrayptrs(py_x);
  y = pyvector_to_Carrayptrs(py_y);
  // Allocate output variables
  py_alpha = (PyArrayObject*) PyArray_SimpleNew(nd, dims, NPY_DOUBLE);
  py_beta = (PyArrayObject*) PyArray_SimpleNew(nd, dims, NPY_DOUBLE);
  alpha = pyvector_to_Carrayptrs(py_alpha);
  beta = pyvector_to_Carrayptrs(py_beta);
  // Allocate internal variables
  p0 = new double[ncap];
  p1 = new double[ncap];
  
  // Call ORTHPOL library function
  orthpol::dlancz(n, ncap, x, y, alpha, beta, ierr, p0, p1);

  // Free memory
  delete [] dims;
  delete [] p0;
  delete [] p1;

  return Py_BuildValue("NNi", py_alpha, py_beta, ierr);
}

static PyObject *
Py_dlob(PyObject *self, PyObject *args)
{
  /* VARIABLES */
  // INPUT
  int n;
  PyArrayObject *py_alpha, *py_beta;
  double *alpha, *beta;
  double aleft, right;
  // OUTPUT
  PyArrayObject *py_zero, *py_weight;
  double *zero, *weight;
  int ierr;
  // INTERNAL
  double *e;
  double *a;
  double *b;
  
  if (!PyArg_ParseTuple(args, "iO!O!dd", &n, &PyArray_Type, &py_alpha, &PyArray_Type, &py_beta, &aleft, &right))
    return NULL;
  if (NULL == py_alpha) return NULL;
  if (NULL == py_beta) return NULL;

  // Check double type
  if (not_doublevector(py_alpha)) return NULL;
  if (not_doublevector(py_beta)) return NULL;

  int nd = 1;
  npy_intp *dims = new npy_intp[2];
  dims[0] = n+2;
  // PyArray to C
  if ((PyArray_DIMS(py_alpha)[0] != dims[0]) or (PyArray_DIMS(py_beta)[0] != dims[0])){
    PyErr_SetString(polymodError, "a and b must contain n+2 coefficients.");
    return Py_BuildValue("iii", 0, 0, 1);
  }
  alpha = pyvector_to_Carrayptrs(py_alpha);
  beta = pyvector_to_Carrayptrs(py_beta);
  // Allocate output variables
  py_zero = (PyArrayObject*) PyArray_SimpleNew(nd, dims, NPY_DOUBLE);
  py_weight = (PyArrayObject*) PyArray_SimpleNew(nd, dims, NPY_DOUBLE);
  zero = pyvector_to_Carrayptrs(py_zero);
  weight = pyvector_to_Carrayptrs(py_weight);
  // Allocate internal variables
  e = new double[n+2];
  a = new double[n+2];
  b = new double[n+2];
  
  // Call ORTHPOL library function
  orthpol::dlob(n, alpha, beta, aleft, right, zero, weight, ierr, e, a, b);

  // Free memory
  delete [] dims;
  delete [] e;
  delete [] a;
  delete [] b;

  return Py_BuildValue("NNi", py_zero, py_weight, ierr);
}

static PyObject *
Py_dmcheb(PyObject *self, PyObject *args)
{
  /* VARIABLES */
  // INPUT
  int n, ncapm, mc, mp;
  PyArrayObject *py_xp, *py_yp;
  double *xp, *yp;
  PyObject *py_callback_func;
  double eps;
  int iq, idelta;
  int finl, finr;
  PyArrayObject *py_endl, *py_endr;
  double *endl, *endr;
  PyArrayObject *py_a, *py_b, *py_fnu;
  double *a, *b, *fnu;
  // OUTPUT
  PyArrayObject *py_alpha, *py_beta;
  double *alpha, *beta;
  int ncap, kount, ierr;
  // INTERNAL
  double *xfer, *wfer;
  double *be, *x, *w, *xm, *wm, *s, *s0, *s1, *s2;
  
  if (!PyArg_ParseTuple(args, "iiiiO!O!O!diiiiO!O!O!O!O!", &n, &ncapm, &mc, &mp, 
			&PyArray_Type, &py_xp, 
			&PyArray_Type, &py_yp,
			&py_callback_func,
			&eps, &iq, &idelta, &finl, &finr,
			&PyArray_Type, &py_endl, 
			&PyArray_Type, &py_endr, 
			&PyArray_Type, &py_a, 
			&PyArray_Type, &py_b, 
			&PyArray_Type, &py_fnu))
    return NULL;
  if (NULL == py_xp) return NULL;
  if (NULL == py_yp) return NULL;
  if (NULL == py_callback_func) return NULL;
  if (NULL == py_endl) return NULL;
  if (NULL == py_endr) return NULL;
  if (NULL == py_a) return NULL;
  if (NULL == py_b) return NULL;
  if (NULL == py_fnu) return NULL;

  // Check double type
  if (not_doublevector(py_xp)) return NULL;
  if (not_doublevector(py_yp)) return NULL;
  if (!PyCallable_Check(py_callback_func)) {
    PyErr_SetString(PyExc_TypeError, "Parameter must be callable");
    return NULL;
  }
  if (not_doublevector(py_endl)) return NULL;
  if (not_doublevector(py_endr)) return NULL;
  if (not_doublevector(py_a)) return NULL;
  if (not_doublevector(py_b)) return NULL;
  if (not_doublevector(py_fnu)) return NULL;

  int nd = 1;
  npy_intp *dims = new npy_intp[2];
  dims[0] = n;
  // Set callback functions
  if (iq == 1) set_dquad_callback(self,Py_BuildValue("(O)",py_callback_func));
  else set_dwf_callback(self,Py_BuildValue("(O)",py_callback_func));
  // PyArray to C
  xp = pyvector_to_Carrayptrs(py_xp);
  yp = pyvector_to_Carrayptrs(py_yp);
  endl = pyvector_to_Carrayptrs(py_endl);
  endr = pyvector_to_Carrayptrs(py_endr);
  a = pyvector_to_Carrayptrs(py_a);
  b = pyvector_to_Carrayptrs(py_b);
  fnu = pyvector_to_Carrayptrs(py_fnu);
  // Allocate output variables
  py_alpha = (PyArrayObject*) PyArray_SimpleNew(nd, dims, NPY_DOUBLE);
  py_beta = (PyArrayObject*) PyArray_SimpleNew(nd, dims, NPY_DOUBLE);
  alpha = pyvector_to_Carrayptrs(py_alpha);
  beta = pyvector_to_Carrayptrs(py_beta);
  // Allocate internal variables
  xfer = new double[ncapm];
  wfer = new double[ncapm];
  be = new double[n];
  x = new double[ncapm];
  w = new double[ncapm];
  xm = new double[mc*ncapm+mp];
  wm = new double[mc*ncapm+mp];
  s = new double[mc*ncapm+mp];
  s0 = new double[mc*ncapm+mp];
  s1 = new double[mc*ncapm+mp];
  s2 = new double[mc*ncapm+mp];
  
  // Call ORTHPOL library function
  orthpol::dmcheb(n, ncapm, mc, mp, xp, yp, eps, iq, idelta, finl, finr, endl, endr, xfer, wfer, a, b, fnu, alpha, beta, ncap, kount, ierr, be, x, w, xm, wm, s, s0, s1, s2);

  // Free memory
  delete [] dims;
  delete [] xfer;
  delete [] wfer;
  delete [] be;
  delete [] x;
  delete [] w;
  delete [] xm;
  delete [] wm;
  delete [] s;
  delete [] s0;
  delete [] s1;
  delete [] s2;

  return Py_BuildValue("NNiii", py_alpha, py_beta, ncap, kount, ierr);
}

static PyObject *
Py_dmcdis(PyObject *self, PyObject *args)
{
  /* VARIABLES */
  // INPUT
  int n, ncapm, mc, mp;
  PyArrayObject *py_xp, *py_yp;
  double *xp, *yp;
  PyObject *py_callback_func;
  double eps;
  int iq, idelta, irout;
  int finl, finr;
  PyArrayObject *py_endl, *py_endr;
  double *endl, *endr;
  // OUTPUT
  PyArrayObject *py_alpha, *py_beta;
  double *alpha, *beta;
  int ncap, kount, ierr, ie;
  // INTERNAL
  double *xfer, *wfer;
  double *be, *x, *w, *xm, *wm, *p0, *p1, *p2;
  
  if (!PyArg_ParseTuple(args, "iiiiO!O!OdiiiiiO!O!", 
			&n, &ncapm, &mc, &mp, 
			&PyArray_Type, &py_xp, 
			&PyArray_Type, &py_yp,
			&py_callback_func,
			&eps, &iq, &idelta, &irout, &finl, &finr,
			&PyArray_Type, &py_endl, 
			&PyArray_Type, &py_endr))			
    return NULL;
  if (NULL == py_xp) return NULL;
  if (NULL == py_yp) return NULL;
  if (NULL == py_callback_func) return NULL;
  if (NULL == py_endl) return NULL;
  if (NULL == py_endr) return NULL;

  // Check double type
  if (not_doublevector(py_xp)) return NULL;
  if (not_doublevector(py_yp)) return NULL;
  if (!PyCallable_Check(py_callback_func)) {
    PyErr_SetString(PyExc_TypeError, "Parameter must be callable");
    return NULL;
  }
  if (not_doublevector(py_endl)) return NULL;
  if (not_doublevector(py_endr)) return NULL;

  int nd = 1;
  npy_intp *dims = new npy_intp[2];
  dims[0] = n;
  // Set callback functions
  if (iq == 1) set_dquad_callback(self,Py_BuildValue("(O)",py_callback_func));
  else set_dwf_callback(self,Py_BuildValue("(O)",py_callback_func));
  // PyArray to C
  xp = pyvector_to_Carrayptrs(py_xp);
  yp = pyvector_to_Carrayptrs(py_yp);
  endl = pyvector_to_Carrayptrs(py_endl);
  endr = pyvector_to_Carrayptrs(py_endr);
  // Allocate output variables
  py_alpha = (PyArrayObject*) PyArray_SimpleNew(nd, dims, NPY_DOUBLE);
  py_beta = (PyArrayObject*) PyArray_SimpleNew(nd, dims, NPY_DOUBLE);
  alpha = pyvector_to_Carrayptrs(py_alpha);
  beta = pyvector_to_Carrayptrs(py_beta);
  // Allocate internal variables
  xfer = new double[ncapm];
  wfer = new double[ncapm];
  be = new double[n];
  x = new double[ncapm];
  w = new double[ncapm];
  xm = new double[mc*ncapm+mp];
  wm = new double[mc*ncapm+mp];
  p0 = new double[mc*ncapm+mp];
  p1 = new double[mc*ncapm+mp];
  p2 = new double[mc*ncapm+mp];
  
  // Call ORTHPOL library function
  orthpol::dmcdis(n, ncapm, mc, mp, xp, yp, eps, iq, idelta, irout, finl, finr, endl, endr, xfer, wfer, alpha, beta, ncap, kount, ierr, ie, be, x, w, xm, wm, p0, p1, p2);

  // Free memory
  delete [] dims;
  delete [] xfer;
  delete [] wfer;
  delete [] be;
  delete [] x;
  delete [] w;
  delete [] xm;
  delete [] wm;
  delete [] p0;
  delete [] p1;
  delete [] p2;

  return Py_BuildValue("NNiiii", py_alpha, py_beta, ncap, kount, ierr, ie);
}

static PyObject *
Py_dradau(PyObject *self, PyObject *args)
{
  /* VARIABLES */
  // INPUT
  int n;
  PyArrayObject *py_alpha, *py_beta;
  double *alpha, *beta;
  double end;
  // OUTPUT
  PyArrayObject *py_zero, *py_weight;
  double *zero, *weight;
  int ierr;
  // INTERNAL
  double *e;
  double *a;
  double *b;
  
  if (!PyArg_ParseTuple(args, "iO!O!d", &n, &PyArray_Type, &py_alpha, &PyArray_Type, &py_beta, &end))
    return NULL;
  if (NULL == py_alpha) return NULL;
  if (NULL == py_beta) return NULL;

  // Check double type
  if (not_doublevector(py_alpha)) return NULL;
  if (not_doublevector(py_beta)) return NULL;

  int nd = 1;
  npy_intp *dims = new npy_intp[2];
  dims[0] = n+1;
  // PyArray to C
  if ((PyArray_DIMS(py_alpha)[0] != dims[0]) or (PyArray_DIMS(py_beta)[0] != dims[0])){
    PyErr_SetString(polymodError, "a and b must contain n+1 coefficients.");
    return Py_BuildValue("iii", 0, 0, 1);
  }
  alpha = pyvector_to_Carrayptrs(py_alpha);
  beta = pyvector_to_Carrayptrs(py_beta);
  // Allocate output variables
  py_zero = (PyArrayObject*) PyArray_SimpleNew(nd, dims, NPY_DOUBLE);
  py_weight = (PyArrayObject*) PyArray_SimpleNew(nd, dims, NPY_DOUBLE);
  zero = pyvector_to_Carrayptrs(py_zero);
  weight = pyvector_to_Carrayptrs(py_weight);
  // Allocate internal variables
  e = new double[n+2];
  a = new double[n+2];
  b = new double[n+2];
  
  // Call ORTHPOL library function
  orthpol::dradau(n, alpha, beta, end, zero, weight, ierr, e, a, b);

  // Free memory
  delete [] dims;
  delete [] e;
  delete [] a;
  delete [] b;

  return Py_BuildValue("NNi", py_zero, py_weight, ierr);
}

static PyObject *
Py_drecur(PyObject *self, PyObject *args)
{
  // INPUT
  int n;
  int ipoly;
  double al;
  double be;
  double *a, *b;
  PyArrayObject *alpha, *beta;
  
  if (!PyArg_ParseTuple(args, "iidd", &n, &ipoly, &al, &be))
    return NULL;

  // OUTPUT
  int nd = 1;
  npy_intp *dims = new npy_intp[2];
  dims[0] = n;
  alpha = (PyArrayObject*) PyArray_SimpleNew(nd, dims, NPY_DOUBLE);
  beta = (PyArrayObject*) PyArray_SimpleNew(nd, dims, NPY_DOUBLE);
  a = pyvector_to_Carrayptrs(alpha);
  b = pyvector_to_Carrayptrs(beta);
  int ierr;
  
  orthpol::drecur(n, ipoly, al, be, a, b, ierr);

  // Free memory
  delete [] dims;

  return Py_BuildValue("NNi", alpha, beta, ierr);
}

static PyObject *
Py_dsti(PyObject *self, PyObject *args)
{
  /* VARIABLES */
  // INPUT
  int n;
  int ncap;
  PyArrayObject *py_x, *py_y;
  double *x, *y;
  // OUTPUT
  PyArrayObject *py_alpha, *py_beta;
  double *alpha, *beta;
  int ierr;
  // INTERNAL
  double *p0;
  double *p1;
  double *p2;
  
  if (!PyArg_ParseTuple(args, "iiO!O!", &n, &ncap, &PyArray_Type, &py_x, &PyArray_Type, &py_y))
    return NULL;
  if (NULL == py_x) return NULL;
  if (NULL == py_y) return NULL;

  // Check double type
  if (not_doublevector(py_x)) return NULL;
  if (not_doublevector(py_y)) return NULL;

  int nd = 1;
  npy_intp *dims = new npy_intp[2];
  dims[0] = n;
  // PyArray to C
  x = pyvector_to_Carrayptrs(py_x);
  y = pyvector_to_Carrayptrs(py_y);
  // Allocate output variables
  py_alpha = (PyArrayObject*) PyArray_SimpleNew(nd, dims, NPY_DOUBLE);
  py_beta = (PyArrayObject*) PyArray_SimpleNew(nd, dims, NPY_DOUBLE);
  alpha = pyvector_to_Carrayptrs(py_alpha);
  beta = pyvector_to_Carrayptrs(py_beta);
  // Allocate internal variables
  p0 = new double[ncap];
  p1 = new double[ncap];
  p2 = new double[ncap];
  
  // Call ORTHPOL library function
  orthpol::dsti(n, ncap, x, y, alpha, beta, ierr, p0, p1, p2);

  // Free memory
  delete [] dims;
  delete [] p0;
  delete [] p1;
  delete [] p2;

  return Py_BuildValue("NNi", py_alpha, py_beta, ierr);
}

/* PyORTHPOL set callback functions declarations */
static PyObject* set_dquad_callback(PyObject *self, PyObject *args)
{
    PyObject *result = NULL;
    PyObject *temp;

    if (PyArg_ParseTuple(args, "O:set_callback", &temp)) {
      if (!PyCallable_Check(temp)) {
	PyErr_SetString(PyExc_TypeError, "parameter must be callable");
	return NULL;
      }
      Py_XINCREF(temp);         /* Add a reference to new callback */
      Py_XDECREF(dquad_callback);  /* Dispose of previous callback */
      dquad_callback = temp;       /* Remember new callback */
      /* Boilerplate to return "None" */
      Py_INCREF(Py_None);
      result = Py_None;
    }

    return result;
}

static PyObject* set_dwf_callback(PyObject *self, PyObject *args)
{
    PyObject *result = NULL;
    PyObject *temp;

    if (PyArg_ParseTuple(args, "O:set_callback", &temp)) {
      if (!PyCallable_Check(temp)) {
	PyErr_SetString(PyExc_TypeError, "parameter must be callable");
	return NULL;
      }
      Py_XINCREF(temp);         /* Add a reference to new callback */
      Py_XDECREF(dwf_callback);  /* Dispose of previous callback */
      dwf_callback = temp;       /* Remember new callback */
      /* Boilerplate to return "None" */
      Py_INCREF(Py_None);
      result = Py_None;
    }

    return result;
}

/* ORTHPOL FORTRAN callback functions definitions */
void dquad_callback_func(int& n, double* x, double* w, int& i, int& ierr){
  PyObject *arglist;
  PyObject *returnlist;

  // INPUT args to Python callback function
  // n, i

  // OUTPUT args from Python callback function
  PyArrayObject *py_x, *py_w;

  // Prepare input arglist
  arglist = Py_BuildValue("ii", n, i);

  // Run Python callback function
  returnlist = PyObject_CallObject(dquad_callback, arglist);

  if (returnlist == NULL) {
    PyErr_SetString(PyExc_TypeError, "Null value returned by user defined function.");
    return;
  }

  // Retrive output and set values
  if (!PyArg_ParseTuple(returnlist, "O!O!i", 
			&PyArray_Type, &py_x, 
			&PyArray_Type, &py_w, 
			&ierr))
    return ;
  if (NULL == py_x) return ;
  if (NULL == py_w) return ;
  // Check double type
  if (not_doublevector(py_x)) return ;
  if (not_doublevector(py_w)) return ;
  // Set FORTRAN x,w
  memcpy(x,pyvector_to_Carrayptrs(py_x),n*sizeof(double));
  memcpy(w,pyvector_to_Carrayptrs(py_w),n*sizeof(double));
}

double dwf_callback_func(double& x, int& i){
  PyObject *arglist = NULL;
  PyObject *returnlist = NULL;

  // OUTPUT args from Python callback function
  double w;

  // Prepare input arglist
  arglist = Py_BuildValue("di", x, i);

  // Run Python callback function
  returnlist = PyObject_CallObject(dwf_callback, arglist);
  Py_DECREF(arglist);

  // int dummy;
  // Retrive output and set values
  if (returnlist == NULL) {
    PyErr_SetString(PyExc_TypeError, "Null value returned by user defined function.");
    return 0.;
  }
  if (!PyArg_ParseTuple(Py_BuildValue("(O)",returnlist), "d", &w)){
    PyErr_SetString(PyExc_TypeError, "Wrong type returned by user defined function.");
    return 0.;
  }
  Py_DECREF(returnlist);

  // RETURN
  return w;
}


/* polymod functions definitions */
static PyObject*
Py_polyeval(PyObject *self, PyObject *args)
{
  /** 
      Evaluate polynomials of the form:
      P_{n+1}(x) = (x - alpha_n)P_{n}(x) - beta_n P_{n-1}(x)
   **/

  /* VARIABLES */
  // INPUT
  int n, normalized; // normalized = 0 False, normalized = 1 True
  PyObject *py_alpha_arg=NULL, *py_beta_arg=NULL; // Recursion coefficients
  PyObject *py_rs_arg=NULL; 	// Evaluation points
  PyArrayObject *py_alpha=NULL, *py_beta=NULL; // Recursion coefficients
  PyArrayObject *py_rs=NULL; 	// Evaluation points
  double *alpha, *beta_j, *beta_jm1, *rs, sqbeta_j, sqbeta_jm1;
  // OUTPUT
  PyArrayObject *py_out;
  // INTERNAL
  npy_intp *dims = new npy_intp[1];
  double *old1=NULL, *old2=NULL, *outinner, *tmp;

  // if (!PyArg_ParseTuple(args, "O!iO!O!i", &PyArray_Type, &py_rs, 
  //                       &n, &PyArray_Type, &py_alpha, &PyArray_Type, &py_beta,
  //                       &normalized))
  //   return NULL;
  // if (NULL == py_rs) return NULL;
  // if (NULL == py_alpha) return NULL;
  // if (NULL == py_beta) return NULL;
  if (!PyArg_ParseTuple(args, "OiOOi", &py_rs_arg, &n, 
			&py_alpha_arg, &py_beta_arg, &normalized))
    return NULL;

  py_rs = (PyArrayObject *)PyArray_FROM_OTF(py_rs_arg, NPY_DOUBLE, 
                                            NPY_ARRAY_C_CONTIGUOUS | NPY_ARRAY_ALIGNED);
  if (py_rs == NULL) return NULL;
  py_alpha = (PyArrayObject *)PyArray_FROM_OTF(py_alpha_arg, NPY_DOUBLE, 
                                               NPY_ARRAY_C_CONTIGUOUS | NPY_ARRAY_ALIGNED);
  if (py_alpha == NULL) goto fail;
  py_beta = (PyArrayObject *)PyArray_FROM_OTF(py_beta_arg, NPY_DOUBLE, 
                                              NPY_ARRAY_C_CONTIGUOUS | NPY_ARRAY_ALIGNED);
  if (py_beta == NULL) goto fail;
  
  if (n < 0)
    PyErr_SetString(polymodError, "The order must be >= 0.");
  if ((PyArray_NDIM(py_rs) > 1) || (PyArray_NDIM(py_alpha) > 1) || (PyArray_NDIM(py_beta) > 1))
    PyErr_SetString(polymodError, "The array provided must be 1 dimensional.");
  if ((PyArray_DIMS(py_alpha)[0] < n) or (PyArray_DIMS(py_beta)[0] < n))
    PyErr_SetString(polymodError, "The recurrence coefficeints must be more than n.");

  dims[0] = PyArray_DIMS(py_rs)[0];

  // Allocate output variables
  py_out = (PyArrayObject *)PyArray_SimpleNew(1, dims, NPY_DOUBLE);

  // Allocate auxiliary space
  outinner = new double[dims[0]];
  
  // Use three term recursion to compute the polynomial
  if (n >= 0) {
    if (normalized == 0){
      for (int i = 0; i < dims[0]; i++) outinner[i] = 1.;
    } else {
      beta_j = (double *)PyArray_GETPTR1(py_beta, 0);
      sqbeta_j = sqrt(*beta_j);
      for (int i = 0; i < dims[0]; i++) outinner[i] = 1./sqbeta_j;
    }
  }
  if (n >= 1) {
    old1 = outinner;		// Copy pointer
    outinner = new double[dims[0]];
    if (normalized == 0){
      alpha = (double *)PyArray_GETPTR1(py_alpha, 0);
      for (int i = 0; i < dims[0]; i++) {
        rs = (double *)PyArray_GETPTR1(py_rs, i);
        outinner[i] = *rs - *alpha;
      }
    } else {
      alpha = (double *)PyArray_GETPTR1(py_alpha, 0);
      beta_j = (double *)PyArray_GETPTR1(py_beta, 1);
      sqbeta_j = sqrt(*beta_j);
      for (int i = 0; i < dims[0]; i++) {
        rs = (double *)PyArray_GETPTR1(py_rs, i);
        outinner[i] = (*rs - *alpha) * old1[i] / sqbeta_j;
      }
    }
  }
  if (n >= 2) {
    old2 = new double[dims[0]];
  }
  for (int j=2; j <= n; j++){
    // Swap pointers
    tmp = old2;
    old2 = old1;
    old1 = outinner;
    outinner = tmp;		// Here we put the new values (save in allocation)
    if (normalized == 0){
      alpha = (double *)PyArray_GETPTR1(py_alpha, j-1);
      beta_jm1 = (double *)PyArray_GETPTR1(py_beta, j-1);
      for (int i = 0; i < dims[0]; i++) {
        rs = (double *)PyArray_GETPTR1(py_rs, i);
        outinner[i] = (*rs - *alpha) * old1[i] - *beta_jm1 * old2[i];
      }
    } else {
      alpha = (double *)PyArray_GETPTR1(py_alpha, j-1);
      beta_j = (double *)PyArray_GETPTR1(py_beta, j);
      beta_jm1 = (double *)PyArray_GETPTR1(py_beta, j-1);
      sqbeta_j = sqrt( *beta_j );
      sqbeta_jm1 = sqrt( *beta_jm1 );
      for (int i = 0; i < dims[0]; i++) {
        rs = (double *)PyArray_GETPTR1(py_rs, i);
        outinner[i] = (*rs - *alpha) * old1[i] / sqbeta_j - 
          sqbeta_jm1 / sqbeta_j * old2[i];
      }
    }
  }

  // Free space and prepare output
  if (old1 != NULL) delete [] old1;
  if (old2 != NULL) delete [] old2;
  
  for (int i = 0; i < dims[0]; i++) {
    double *v = (double *)PyArray_GETPTR1(py_out, i);
    *v = outinner[i];
  }

  delete [] outinner;
  delete [] dims;
  
  Py_DECREF(py_rs);
  Py_DECREF(py_alpha);
  Py_DECREF(py_beta);
  return Py_BuildValue("N", py_out);

 fail:
  Py_XDECREF(py_rs);
  Py_XDECREF(py_alpha);
  Py_XDECREF(py_beta);
  return NULL;
}

static PyObject*
Py_monomials(PyObject *self, PyObject *args)
{
  /**
     Evaluate the monomials coefficients from the recursion coefficients
   **/

  /* VARIABLES */
  // INPUT
  int normalized; // normalized = 0 False, normalized = 1 True
  PyObject *py_alpha_arg=NULL, *py_beta_arg=NULL; // Recursion coefficients
  PyArrayObject *py_alpha=NULL, *py_beta=NULL; // Recursion coefficients
  double *alpha_m1, *beta, *beta_m1, sqbeta, sqbeta_m1;
  // OUTPUT
  PyArrayObject *py_out;
  // INTERNAL
  npy_intp *na = new npy_intp[1];
  npy_intp *nb = new npy_intp[1];
  npy_intp *dim = new npy_intp[1];
  double *old1=NULL, *old2=NULL, *outinner, *tmp;

  if (!PyArg_ParseTuple(args, "OOi", &py_alpha_arg, &py_beta_arg, &normalized))
    return NULL;

  py_alpha = (PyArrayObject *)PyArray_FROM_OTF(py_alpha_arg, NPY_DOUBLE, 
                                               NPY_ARRAY_C_CONTIGUOUS | NPY_ARRAY_ALIGNED);
  if (py_alpha == NULL) goto fail;
  py_beta = (PyArrayObject *)PyArray_FROM_OTF(py_beta_arg, NPY_DOUBLE, 
                                              NPY_ARRAY_C_CONTIGUOUS | NPY_ARRAY_ALIGNED);
  if (py_beta == NULL) goto fail;

  if ((PyArray_NDIM(py_alpha) > 1) || (PyArray_NDIM(py_beta) > 1))
    PyErr_SetString(polymodError, "Array alpha and beta provided must be 1 dimensional.");  
  na[0] = PyArray_DIMS(py_alpha)[0];
  nb[0] = PyArray_DIMS(py_beta)[0];
  if (na[0] != nb[0])
    PyErr_SetString(polymodError, "The size of alpha and beta must be the same");
  dim[0] = na[0];

  // Allocate output variables
  py_out = (PyArrayObject *)PyArray_SimpleNew(1, dim, NPY_DOUBLE);

  // Auxiliary space
  outinner = new double[dim[0]];
  for (int i=0; i < dim[0]; i++) outinner[i] = 0.;

  // Unroll three term recursion to compute coefficients
  if (dim[0] > 0){
    if (normalized == 0){ 
      outinner[0] = 1.;
    } else {
      beta = (double *)PyArray_GETPTR1(py_beta, 0);
      sqbeta = sqrt(*beta);
      outinner[0] = 1./sqbeta;
    }
  }

  if (dim[0] > 1){
    old1 = outinner;  
    outinner = new double[dim[0]];
    for (int i=0; i < dim[0]; i++) outinner[i] = 0.;
    if (normalized == 0){
      alpha_m1 = (double *)PyArray_GETPTR1(py_alpha, 0);
      outinner[0] = - *alpha_m1;
      outinner[1] = 1.;
    } else {
      alpha_m1 = (double *)PyArray_GETPTR1(py_alpha, 0);
      beta = (double *)PyArray_GETPTR1(py_beta, 1);
      sqbeta = sqrt(*beta);
      outinner[0] = - *alpha_m1 / sqbeta * old1[0];
      outinner[1] = old1[0] / sqbeta;
    }
  }

  if (dim[0] > 2){
    old2 = new double[dim[0]];
    for (int i=0; i < dim[0]; i++) old2[i] = 0.;
  }
  for (int j=2; j < dim[0]; j++){
    // Swap
    tmp = old2;
    old2 = old1;
    old1 = outinner;
    outinner = tmp;
    if (normalized == 0){
      alpha_m1 = (double *)PyArray_GETPTR1(py_alpha, j-1);
      beta_m1 = (double *)PyArray_GETPTR1(py_beta, j-1);
      outinner[0] = - *alpha_m1 * old1[0] - *beta_m1 * old2[0];
      for (int k=1; k <= j; k++)
	outinner[k] = old1[k-1] - *alpha_m1 * old1[k] - *beta_m1 * old2[k];
    } else {
      alpha_m1 = (double *)PyArray_GETPTR1(py_alpha, j-1);
      beta_m1 = (double *)PyArray_GETPTR1(py_beta, j-1);
      beta = (double *)PyArray_GETPTR1(py_beta, j);
      sqbeta_m1 = sqrt( *beta_m1 );
      sqbeta = sqrt( *beta );
      outinner[0] = ( - *alpha_m1 * old1[0] - sqbeta_m1 * old2[0] ) / sqbeta;
      for (int k=1; k <= j; k++)
	outinner[k] = (old1[k-1] - *alpha_m1 * old1[k] - sqbeta_m1 * old2[k]) / sqbeta;
    }
  }
  
  // Free space and prepare output
  if (old1 != NULL) delete [] old1;
  if (old2 != NULL) delete [] old2;
  
  for (int i = 0; i < dim[0]; i++) {
    double *v = (double *)PyArray_GETPTR1(py_out, i);
    *v = outinner[i];
  }

  delete [] outinner;
  delete [] dim;
  
  Py_DECREF(py_alpha);
  Py_DECREF(py_beta);
  return Py_BuildValue("N", py_out);

 fail:
  Py_XDECREF(py_alpha);
  Py_XDECREF(py_beta);
  return NULL;
}

static PyObject*
Py_numeric_gamma(PyObject *self, PyObject *args)
{
  /* VARIABLES */
  // INPUT
  int n;
  PyArrayObject *py_alpha, *py_beta; // Recursion coefficients
  double *alpha, *beta;
  // OUTPUT
  double sqnrm;
  // INTERNAL
  double *tmp, *nrmpol, *nrmold1=NULL, *nrmold2=NULL;
  double *zeros, *weights, *e;
  int nrmpts, ierr;

  if (!PyArg_ParseTuple(args, "iO!O!", &n, &PyArray_Type, &py_alpha, &PyArray_Type, &py_beta))
    return NULL;
  if (NULL == py_alpha) return NULL;
  if (NULL == py_beta) return NULL;
  
  if (n < 0)
    PyErr_SetString(polymodError, "The order must be >= 0.");
  if ((PyArray_NDIM(py_alpha) > 1) || (PyArray_NDIM(py_beta) > 1))
    PyErr_SetString(polymodError, "The array provided must be 1 dimensional.");
  if ((PyArray_DIMS(py_alpha)[0] < n) or (PyArray_DIMS(py_beta)[0] < n))
    PyErr_SetString(polymodError, "The recurrence coefficeints must be more than n.");
  
  // PyArray to C
  alpha = pyvector_to_Carrayptrs(py_alpha);
  beta = pyvector_to_Carrayptrs(py_beta);

  // Internal normalization variables
  nrmpts = n+1;
  zeros = new double[nrmpts];
  weights = new double[nrmpts];
  e = new double[nrmpts];
  // Call ORTHPOL library function
  orthpol::dgauss(nrmpts, alpha, beta, zeros, weights, ierr, e);
  if (ierr != 0)
    PyErr_SetString(polymodError, "Error in the generation of the Gauss points.");
  delete [] e;
  // Allocate normalization polynomial
  nrmpol = new double[nrmpts];

  // Use three term recursion to compute the unnormalized polynomial
  // and the normalizing polynomial
  if (n >= 0) {
    for (int i = 0; i < nrmpts; i++) nrmpol[i] = 1.;
  }
  if (n >= 1) {
    nrmold1 = nrmpol;		// Copy pointer
    nrmpol = new double[nrmpts];
    for (int i = 0; i < nrmpts; i++) nrmpol[i] = zeros[i] - alpha[0];
  }
  if (n >= 2) {
    nrmold2 = new double[nrmpts];
  }
  for (int j=2; j <= n; j++){
    // Swap pointers
    tmp = nrmold2;
    nrmold2 = nrmold1;
    nrmold1 = nrmpol;
    nrmpol = tmp;
    for (int i = 0; i < nrmpts; i++)
      nrmpol[i] = (zeros[i] - alpha[j-1]) * nrmold1[i] - beta[j-1] * nrmold2[i];
  }

  // Compute normalization constant
  sqnrm = 0.;
  for (int i = 0; i < nrmpts; i++)
    sqnrm += nrmpol[i] * nrmpol[i] * weights[i];
  
  // Free space and prepare output
  if (nrmold1 != NULL) delete [] nrmold1;
  if (nrmold2 != NULL) delete [] nrmold2;
  delete [] nrmpol;
  delete [] zeros;
  delete [] weights;
  
  return Py_BuildValue("d", sqnrm);

}

static PyObject*
Py_vandermonde(PyObject *self, PyObject *args)
{
  /* VARIABLES */
  // INPUT
  int n;
  PyArrayObject *py_alpha, *py_beta; // Evaluation points
  PyArrayObject *py_rs; 	// Evaluation points
  double *alpha, *beta, *rs;
  // OUTPUT
  PyArrayObject *py_out;
  double **out;
  // INTERNAL
  npy_intp *dims = new npy_intp[2];
  double **nrmpol;
  double *zeros, *weights, *e;

  if (!PyArg_ParseTuple(args, "O!iO!O!", &PyArray_Type, &py_rs, &n, &PyArray_Type, &py_alpha, &PyArray_Type, &py_beta))
    return NULL;
  if (NULL == py_rs) return NULL;
  if (NULL == py_alpha) return NULL;
  if (NULL == py_beta) return NULL;
  
  if (n < 0)
    PyErr_SetString(polymodError, "The order must be bigger than 0.");
  if ((PyArray_NDIM(py_rs) > 1) || (PyArray_NDIM(py_alpha) > 1) || (PyArray_NDIM(py_beta) > 1))
    PyErr_SetString(polymodError, "The array provided must be 1 dimensional.");
  if ((PyArray_DIMS(py_alpha)[0] < n) or (PyArray_DIMS(py_beta)[0] < n))
    PyErr_SetString(polymodError, "The recurrence coefficeints must be more than n.");
  
  dims[0] = PyArray_DIMS(py_rs)[0];
  dims[1] = n+1;

  // PyArray to C
  rs = pyvector_to_Carrayptrs(py_rs);
  alpha = pyvector_to_Carrayptrs(py_alpha);
  beta = pyvector_to_Carrayptrs(py_beta);

  // Allocate output variables
  py_out = (PyArrayObject*) PyArray_SimpleNew(2, dims, NPY_DOUBLE);
  out = pymatrix_to_Carrayptrs(py_out);

  // Internal normalization variables
  int nrmpts = n+1;
  zeros = new double[nrmpts];
  weights = new double[nrmpts];
  e = new double[nrmpts];
  int ierr;
  // Call ORTHPOL library function
  orthpol::dgauss(nrmpts, alpha, beta, zeros, weights, ierr, e);
  if (ierr != 0)
    PyErr_SetString(polymodError, "Error in the generation of the Gauss points.");
  delete [] e;
  // Allocate normalization polynomial
  nrmpol = new double*[nrmpts];
  for (int i = 0; i < nrmpts; i++)
    nrmpol[i] = new double[nrmpts];
  
  // Use three term recursion to compute the unnormalized polynomial
  // and the normalizing polynomial
  if (n >= 0) {
    for (int i = 0; i < dims[0]; i++) out[i][0] = 1.;
    for (int i = 0; i < nrmpts; i++) nrmpol[i][0] = 1.;
  }
  if (n >= 1) {
    for (int i = 0; i < dims[0]; i++) out[i][1] = rs[i] - alpha[0];
    for (int i = 0; i < nrmpts; i++) nrmpol[i][1] = zeros[i] - alpha[0];
  }
  for (int i = 0; i < dims[0]; i++)
    for (int j=2; j <= n; j++)
      out[i][j] = (rs[i] - alpha[j-1]) * out[i][j-1] - beta[j-1] * out[i][j-2];
  for (int i = 0; i < nrmpts; i++)
    for (int j=2; j <= n; j++)
      nrmpol[i][j] = (zeros[i] - alpha[j-1]) * nrmpol[i][j-1] - beta[j-1] * nrmpol[i][j-2];

  // Normalize
  double *sqnrm = new double[nrmpts];
  for (int j = 0; j < nrmpts; j++) sqnrm[j] = 0.;
  for (int i = 0; i < nrmpts; i++){
    for (int j = 0; j < nrmpts; j++)
      sqnrm[j] += nrmpol[i][j] * nrmpol[i][j] * weights[i];
  }
  for (int j = 0; j < nrmpts; j++) sqnrm[j] = sqrt(sqnrm[j]);
  for (int i = 0; i < dims[0]; i++)
    for (int j = 0; j < nrmpts; j++)
      out[i][j] /= sqnrm[j];

  // Free space and prepare output
  delete [] nrmpol;
  delete [] zeros;
  delete [] weights;
  free_Carrayptrs(out);
  
  return PyArray_Return(py_out);
}
