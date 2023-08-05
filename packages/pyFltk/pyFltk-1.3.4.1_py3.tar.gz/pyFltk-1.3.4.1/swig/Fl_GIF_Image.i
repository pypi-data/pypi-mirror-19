/* File : Fl_GIF_Image.i */
//%module Fl_GIF_Image

%feature("docstring") ::Fl_GIF_Image
"""
The Fl_GIF_Image class supports loading, caching, and drawing of Compuserve 
GIF images. The class loads the first image and supports transparency.
""" ;

%{
#include "FL/Fl_GIF_Image.H"
%}

//%include "macros.i"
//CHANGE_OWNERSHIP(Fl_GIF_Image)

%include "FL/Fl_GIF_Image.H"
