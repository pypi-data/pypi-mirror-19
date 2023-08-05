/* File : Fl_Bitmap.i */
//%module Fl_Bitmap

%feature("docstring") ::Fl_Bitmap
"""
The Fl_Bitmap class supports caching and drawing of mono-color 
(bitmap) images. Images are drawn using the current color.
"""  ;

%{
#include "FL/Fl_Bitmap.H"
%}

%typemap(in) const uchar *bits {
    /* Check if the input support the buffer protocol */
    Py_ssize_t size_buffer;
    const void * buffer;
    int failure = PyObject_AsReadBuffer($input,&buffer,&size_buffer);
    if (!failure) {
      // work with array object
      $1 = (uchar *) buffer;
    } else {
       // work with list object
       // clear the error from PyObject_AsReadBuffer
       PyErr_Clear();
       size_buffer=0;
       buffer=0;
       /* Check if is a list */
       if (PyList_Check($input)) {
         int size = PyList_Size($input);
         int i = 0;
         $1 = (uchar *) malloc((size+1)*sizeof(char));
         for (i = 0; i < size; i++) {
		PyObject *o = 	PyList_GetItem($input,i);
           if (PyInt_Check(o))
             $1[i] = (char)PyInt_AsLong(o);
           else {
             PyErr_SetString(PyExc_TypeError,"list must contain ints");
             free($1);
             return NULL;
           }
         }
         $1[i] = 0;
       } else {
         PyErr_SetString(PyExc_TypeError,"not a list or does not support single-segment readable buffer interface");
         return NULL;
       }
     }
}


%ignore Fl_Bitmap::Fl_Bitmap(const char *bits, int W, int H);
%ignore Fl_Bitmap::id;

//%include "macros.i"
//CHANGE_OWNERSHIP(Fl_Bitmap)

%include "FL/Fl_Bitmap.H"



