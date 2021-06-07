**************
The core files
**************

The labphew core files are necessary for consistency of new applications with the overall architecture of the
package and other system program. Although we recomment editting the labphew code for customizing to your needs
if you do not absolutely need to change part of the core syntax, please don't. Following the conventions and base
classes in the labphew core directly allows for easier integration of new modules or new instruments.

base
----

Contains the base classes for defining a model for a certain class of instruments and devices. The methods in
this class are essential for connecting to the other layers of labphew. The methods are defined following a certain
logic which might not be the optimum for all types of instruments of applications such as high-speed acquisition or
synchronized measurements.

defaults
--------

Since the labphew ``Operator`` gets its parameters from a configuration file, some templates are generated to
allow out of the box execution of commands or to serve as a template for customized applications.

tools
-----

Small pieces of code that come handy in some of the labphew modules but does not belong to a certain layer are stored here.