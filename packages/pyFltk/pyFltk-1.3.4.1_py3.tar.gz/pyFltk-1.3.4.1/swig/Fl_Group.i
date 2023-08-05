/* File : Fl_Group.i */
//%module Fl_Group

%feature("docstring") ::Fl_Group
"""
The Fl_Group class is the FLTK container widget. It maintains an array of 
child widgets. These children can themselves be any widget including Fl_Group. 
The most important subclass of Fl_Group  is Fl_Window, however groups can 
also be used to control radio buttons or to enforce resize behavior.
""" ;

%{
#include "FL/Fl_Group.H"
%}

%include "macros.i"

CHANGE_OWNERSHIP(Fl_Group)

REVERT_OWNERSHIP(Fl_Group::add)

REVERT_OWNERSHIP(Fl_Group::remove)

%ignore Fl_Group::find(const Fl_Widget*) const;
%ignore Fl_Group::add(Fl_Widget&);
%ignore Fl_Group::remove(Fl_Widget&);
%ignore Fl_Group::resizable(Fl_Widget& o);
%rename(insert_before) Fl_Group::insert(Fl_Widget& o, Fl_Widget* before);

// needed for getting directors to work
%ignore Fl_Group::array() const;

%include "FL/Fl_Group.H"


