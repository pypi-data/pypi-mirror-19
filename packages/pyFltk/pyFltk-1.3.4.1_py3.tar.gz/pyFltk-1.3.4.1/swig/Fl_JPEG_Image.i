/* File : Fl_JPEG_Image.i */
//%module Fl_JPEG_Image

%feature("docstring") ::Fl_JPEG_Image
"""
The Fl_JPEG_Image class supports loading, caching, and drawing of Joint 
Photographic Experts Group (JPEG) File Interchange Format (JFIF) images. 
The class supports grayscale and color (RGB) JPEG image files.
""" ;

%{
#include "FL/Fl_JPEG_Image.H"
%}

//%include "macros.i"
//CHANGE_OWNERSHIP(Fl_JPEG_Image)

%include "FL/Fl_JPEG_Image.H"
