**************
How to labphew
**************

Once you have installed labphew and its dependencies and made yourself familiar with the folder structure,
you perhaps want to run a measurement. If the hardware you want to use is among :doc:`./devices`, tailoring
the existing code is perhaps the easiest way forward.

For not-supported devices, see :doc:`./customize`.

Running an example
==================

Each of the Python scripts in labphew are written in a way that you can directly execute them
and something simple will happen. These direct calls serve as examples of using the functions inside the files.
Most of these files however are libraries or classes that have to be called from another code. This structure
makes labphew is capable of both scripted and interactive measurements. Scripted measurements are faster to
develop and are ideal for accumulating statistics once the setup is properly characterised.
Interactive measurement programs require developers to be familiar with user-interface design.

The coding layer that is closest to the user, in the labphew folder structure, is view.
The chain of calling functions (usually) starts at ``view/start.py``, so if you want to figure out the hierarchy of commands,
look for the functions that called for in that file.

The default devices in labphew are also accompanied with a dummy version, and ``Operator`` that simulates the basic
functions of that device. If you do not have the physical device in hand, you can play quite a bit with the code by
using the dummy models.

Tailoring an existing model
===========================

When completed, labphew provides basic support for two devices:
+ Digilent Analog Discovery 2: an advanced data acquisition card
+ Basler camera: a group of cameras that can be controlled by the `pypylon wrapper <https://github.com/basler/pypylon>`_

The controllers for both of these devices are partially complete, which means you might need to extend the controller
to gain access to some of their functionalities. The most basic functions are, however, already in the controller.
Therefore, the first code you need to hack is actually the model file.


