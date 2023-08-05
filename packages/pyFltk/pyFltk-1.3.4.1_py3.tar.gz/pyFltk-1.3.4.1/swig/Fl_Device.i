/* File : Fl_Device.i */

%feature("docstring") ::Fl_Device
"""
Declaration of classes Fl_Device, Fl_Graphics_Driver, Fl_Surface_Device, 
 Fl_Display_Device, Fl_Device_Plugin.
All graphical output devices and all graphics systems.
""" ;

%{
#include "FL/Fl_Device.H"
%}

//%include "macros.i"

//CHANGE_OWNERSHIP(Fl_Device)
%ignore Fl_Xlib_Graphics_Driver;
%ignore Fl_Quartz_Graphics_Driver;
%ignore Fl_GDI_Graphics_Driver;

%include "FL/Fl_Device.H"
