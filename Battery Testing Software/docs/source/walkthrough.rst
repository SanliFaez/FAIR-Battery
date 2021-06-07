*******************
A short guided tour
*******************

This short guide walks you through the folder structure of the labphew package and introduces you to the main
classes and functions that you might want to tinker with

.. image:: _static/mvc_diagram.png
   :scale: 50 %
   :alt: the model-view-controller framework

labphew is developed following the Model-View-Controller (MVC) structure.
In this structure the code is separated into different subfolders,
with a clear separation of tasks. These modules and their interactions with the user and electronics
are schematically presented in the figure above. The MVC subfolders can be explained as follows:

* *model*: Specifies the logic and the order of operations to perform a certain measurement.
* *view*: User-facing elements, such as the graphical user interface (GUI), or the command-line interface (CLI).
* *controller*: The drivers for the hardware. These modules handle the low-level communication with the devices.

Additional to the MVC subfolders, labphew has three subfolder for managing communication with users

* *core*: Includes the templates and base classes that are introduced for inter-operability.
* *docs*: Contains the documentation, such as this file
* *Examples*: a few examples of labphew applications written for generic or special purposes

To further understand the architecture of the code, we specify some of the main contents of each module.

Controller
^^^^^^^^^^

The controllers can be regarded as the drivers for devices, or the Python wrappers for these drivers.
Manufacturers of hardware sometimes offer the drivers, such as `PyPylon <https://github.com/basler/pypylon>`_
for Basler cameras or `NIDAQmx <https://github.com/ni/nidaqmx-python/>`_ for National Instruments cards.
Often, drivers are developed by other researchers and can be find on github.
Sometimes there is no available driver for the cameras and the user will need to develop their own.

Learn more about the labphew basic controllers in :doc:`./labphew.controller`

Model
^^^^^

Models translate the logic of the measurement into machine-iterable algorithms that communicate with
the devices using the controller module. Each model contains an ``Operator`` class
(remember the Operator in the Matrix series?).
A simple case could be capturing a single frame with a camera
in which it is usually needed to open a shutter, trigger the camera, acquire a frame, close the shutter,
and readout the acquired data and save or display.
This specific sequence of operation are determined by the user
and thus should be separated from the controllers.
In labphew, this procedure is included in various method of the Operator class, for example
``read_frame`` which starts a captures and displays a single frame,
or ``record_sequence`` which continuously saves the acquired images to the hard drive.

You can read more about the labphew standard models in :doc:`./labphew.model`

View
^^^^

The view folder is the collection of interfaces for users to run an experiment. Different views can be written for the
same model, dependent on how the user likes to interact with the setup. A generic view can also work with different
models. A view module is usually initiated by calling an ``Operator`` to take care of the communication with devices
and the steps of the main control loop.
Views can be both working with command-line interface (CLI) or a graphical user interface (GUI).

Read more about how to navigate through the labphew view modules in :doc:`./labphew.view`

How to play
^^^^^^^^^^^

If you have already installed labphew, here are some suggestions on :doc:`./howtolabphew`.

Otherwise, see :doc:`./installation`
