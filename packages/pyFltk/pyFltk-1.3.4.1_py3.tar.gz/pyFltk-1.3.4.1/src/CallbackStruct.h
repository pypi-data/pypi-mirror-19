// This struct manages callbacks into Python.  It is stored as the
// user data portion of a widget, and the PythonCallback function is
// set as the callback.  PythonCallback unmarshalls the pointer to
// the Python function and Python user data and calls back into
// Python. 
// 

#ifndef CallbackStruct_h
#define CallbackStruct_h

#include <Python.h>

class CallbackStruct
{
public:
  PyObject *func;
  PyObject *data;
  PyObject *widget;
  void     *type;
  PyObject *link;
  CallbackStruct( PyObject *theFunc, PyObject *theData, PyObject *theWidget, PyObject *theLink = 0):
    func(theFunc),
    data(theData),
    widget(theWidget)
  {}
  CallbackStruct( PyObject *theFunc, PyObject *theData, void *theType):
    func(theFunc),
    data(theData),
    widget(0),
    type(theType)
  {}
  
};

#endif
