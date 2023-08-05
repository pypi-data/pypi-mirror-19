/* File : Fl_Widget.i */
//%module Fl_Widget

%feature("docstring") ::Fl_Widget
"""
Fl_Widget is the base class for all widgets in FLTK. You can't create one of 
these because the constructor is not public. However you can subclass it.

All 'property' accessing methods, such as color(), parent(), or argument() 
are implemented as trivial inline functions and thus are as fast and small 
as accessing fields in a structure. Unless otherwise noted, the property 
setting methods such as color(n) or label(s) are also trivial inline 
functions, even if they change the widget's appearance. It is up to the user 
code to call redraw() after these. 
""" ;

%{
#include <FL/Fl.H>
#include "FL/Fl_Widget.H"
%}

%include "macros.i"

CHANGE_OWNERSHIP(Fl_Widget)

%pythonappend Fl_Widget::image(Fl_Image *a) %{
        if len(args) > 0:
            #delegate ownership to C++
            self.my_image = args[0]
%}
%pythonappend Fl_Widget::deimage(Fl_Image *a) %{
        if len(args) > 0:
            #delegate ownership to C++
            self.my_deimage = args[0]
%}

%pythonappend Fl_Widget::label %{
        if len(args) > 0:
            self.my_label = args[len(args)-1]
%}


%{
#include "CallbackStruct.h"
#include <FL/Fl_Button.H>

  //static PyObject *my_pycallback = NULL;
  static void PythonCallBack(Fl_Widget *widget, void *clientdata)
    {
      PyObject *func, *arglist;
      PyObject *result;
      PyObject *obj = 0;
      CallbackStruct* cb = (CallbackStruct*)clientdata;

      // This is the function .... 
      func = cb->func;

      if (cb->widget != 0) {
        // the parent widget
        obj = (PyObject *)( ((CallbackStruct *)clientdata)->widget);
      }
      else if (cb->type != 0) {
        // this is the type of widget
        swig_type_info *descr = (swig_type_info *)cb->type;
        if (descr != 0) {
          //printf("success\n");
          obj = SWIG_NewPointerObj(widget, (swig_type_info *)descr, 0);
        }
      }
      if (obj == 0) {
        // generic fallback
        obj = SWIG_NewPointerObj(widget, SWIGTYPE_p_Fl_Widget, 0);
      }

      if (((CallbackStruct *)clientdata)->data)
	{
	  arglist = Py_BuildValue("(OO)", obj, (PyObject *)(((CallbackStruct *)clientdata)->data) ); 
	}
      else
	{
	  arglist = Py_BuildValue("(O)", obj ); 
	}

      result =  PyEval_CallObject(func, arglist);
   
      //Py_XDECREF(arglist);                           // Trash arglist
      Py_XDECREF(result);
      if (PyErr_Occurred())
	{
	  PyErr_Print();
	}
   
      return /*void*/;
    }
  %}

%ignore Fl_Widget::image(Fl_Image& a);
%ignore Fl_Widget::deimage(Fl_Image& a);
//%ignore Fl_Widget::label;

%include "FL/Fl_Widget.H"




%extend Fl_Widget {
#include <FL/Fl_Window.H>
#include <FL/Fl_Image.H>

 // reimplementing protected member draw_label()
 void draw_label()
 {
   int X = self->x()+Fl::box_dx(self->box());
   int W = self->w()-Fl::box_dw(self->box());
   if (W > 11 && self->align()&(FL_ALIGN_LEFT|FL_ALIGN_RIGHT)) {X += 3; W -= 6;}
   self->draw_label(X, self->y()+Fl::box_dy(self->box()), W, self->h()-Fl::box_dh(self->box()),self->align());
 }

 // reimplementing protected member draw_label()
 void draw_backdrop()
 {
   if (self->align() & FL_ALIGN_IMAGE_BACKDROP) {
    const Fl_Image *img = self->image();
    // if there is no image, we will not draw the deimage either
    if (img && self->deimage() && !self->active_r())
      img = self->deimage();
    if (img) 
      ((Fl_Image*)img)->draw(self->x()+(self->w()-img->w())/2, self->y()+(self->h()-img->h())/2);
   }
 }

 

  void
    callback(PyObject *PyFunc, PyObject *PyWidget, PyObject *PyData = 0)
    {
      //CallbackStruct *cb = 0;
      CallbackStruct *cb = (CallbackStruct*)self->user_data();

      if (cb) {
	cb->func = PyFunc;
	cb->widget = PyWidget;
	if (PyData) {
	  cb->data = PyData;
	}
	cb->widget = PyWidget;
      }
      else
	cb = new CallbackStruct( PyFunc, PyData, PyWidget );

      // Add a reference to new callback
      Py_INCREF(PyFunc);			
      Py_XINCREF(PyData);
      Py_XINCREF(PyWidget);

      self->callback(PythonCallBack, (void *)cb);

    
    }
 
   void
    user_data(PyObject *PyData)
    {
      
      // Add a reference to new callback
      Py_XINCREF(PyData);
	
      CallbackStruct *cb = (CallbackStruct*)self->user_data();
      if (cb == NULL) {
	cb = new CallbackStruct(0, PyData, (PyObject*)0);
	self->user_data((void *)cb);
      }
      else {
	cb->data = PyData;
      }
    
    }

  PyObject* user_data() {
    PyObject *obj = 0;
    CallbackStruct *cb = (CallbackStruct*)self->user_data();
    if (cb) {
      if (cb->data) {
	obj = (PyObject*)cb->data;
      }
    }

    //Py_XDECREF(obj);
    Py_XINCREF(obj);
    return obj;
  }
}


%typemap(in) PyObject *PyFunc {
  if (!PyCallable_Check($input)) {
    PyErr_SetString(PyExc_TypeError, "Need a callable object!");
    return NULL;
  }
  $1 = $input;
}



