/* File : Fl_File_Chooser.i */
//%module Fl_File_Chooser

%feature("docstring") ::Fl_File_Chooser
"""
The Fl_File_Chooser widget displays a standard file selection dialog that 
supports various selection modes.

The Fl_File_Chooser class also exports several static values that may be used 
to localize or customize the appearance of all file chooser dialogs:
Member 	Default value
add_favorites_label 	'Add to Favorites'
all_files_label 	'All Files (*)'
custom_filter_label 	'Custom Filter'
existing_file_label 	'Please choose an existing file!'
favorites_label 	'Favorites'
filename_label 		'Filename:'
filesystems_label 	'My Computer' (WIN32)
			'File Systems' (all others)
manage_favorites_label 	'Manage Favorites'
new_directory_label 	'New Directory?'
new_directory_tooltip 	'Create a new directory.'
preview_label 		'Preview'
save_label 		'Save'
show_label 		'Show:'
sort 			fl_numericsort

The sort member specifies the sort function that is used when loading the 
contents of a directory. 
""" ;

%{
#include "FL/Fl_File_Chooser.H"
%}

//%include "macros.i"
//CHANGE_OWNERSHIP(Fl_File_Chooser)

%ignore Fl_File_Chooser::sort;
// this is not declared on all systems!
%ignore Fl_File_Chooser::rescan_keep_filename;

%{
#include "CallbackStruct.h"

static void PythonCallBack(Fl_File_Chooser *widget, void *clientdata)
{
   PyObject *func, *arglist;
   PyObject *result;
   PyObject *obj;

   func = (PyObject *)( ((CallbackStruct *)clientdata)->func);
   // the parent widget
   obj = (PyObject *)( ((CallbackStruct *)clientdata)->widget);
   //obj = SWIG_NewPointerObj(widget, SWIGTYPE_p_Fl_File_Chooser, 0);
   
   if (((CallbackStruct *)clientdata)->data)
   {
     arglist = Py_BuildValue("(OO)", obj, (PyObject *)(((CallbackStruct *)clientdata)->data) ); 
   }
   else
   {
     arglist = Py_BuildValue("(O)", obj ); 
   }
   result =  PyEval_CallObject(func, arglist);
   
   Py_DECREF(arglist);                           // Trash arglist
   Py_XDECREF(result);
   if (PyErr_Occurred())
   {
	PyErr_Print();
   }
   
   return /*void*/;
}
%}


%include "FL/Fl_File_Chooser.H"

%extend Fl_File_Chooser {
void
callback(PyObject *PyFunc, PyObject *PyWidget, PyObject *PyData = 0)
{
        CallbackStruct *cb = 0;
	cb = new CallbackStruct( PyFunc, PyData, PyWidget );

	Py_INCREF(PyFunc);			/* Add a reference to new callback */
        Py_XINCREF(PyData);
        Py_XINCREF(PyWidget);
	
	self->callback(PythonCallBack, (void *)cb);
    
}
}

%typemap(in) PyObject *PyFunc {
  if (!PyCallable_Check($input)) {
      PyErr_SetString(PyExc_TypeError, "Need a callable object!");
      return NULL;
  }
  $1 = $input;
}

