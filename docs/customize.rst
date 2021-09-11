*************
Customization
*************

While one of the goals of this project is to reduce variation in testing methods, this software and hardware is still
open source, and very open to improvement!

Every measurement setup of protocol has its own logic and requirements.
Therefore, unless you have very basic requirements for your measurements, labphew is meant to be
hacked/customized/edited before is can match your needs. If you are an experienced python programmer,
you can customize labphew by editing the code at any level you need. Hopefully, there is enough value
in the current code that helps you not to start from a blank page.

If you are still in the learning phase, or would like to stay compatible with the existing modules of labphew
these recommendations might help you in getting your desired features rather quickly.

Software Structure
******************
In order to get you started quickly, below is a quick summary of how the code is structured.
For a more in depth explanation of how this project's software is structured, see
the `labphew documentation <https://labphew.readthedocs.io/en/latest/walkthrough.html>`_.


Summarized, the the software follows a Model, View, Controller structure.

.. image:: _static/mvc_diagram.png
   :scale: 50 %
   :alt: the model-view-controller framework

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

The controller can be regarded as the driver for the device, or the Python wrappers for the driver.
For the AD2 this is: ``labphew/controller/waveforms:``

The waveforms controller (DfwController) is a module that implements many of the the basic functionalities for
controlling the AD2 board, inherited from the dwf library provided by Digilent. Examples include setting analog outputs
channels or reading from oscilloscope input channels. Many of these features have been implemented, but the controller
is not complete, so this could be expanded upon if needed.

Model
^^^^^

Models translate the logic of the measurement into machine-iterable algorithms that communicate with
the devices using the controller module. Each model contains an ``Operator`` class
(remember the Operator in the Matrix series?).
A simple example could be capturing a single frame with a camera
in which it is usually needed to open a shutter, trigger the camera, acquire a frame, close the shutter,
and readout the acquired data and save or display.
This specific sequence of operation are determined by the user
and thus should be separated from the controllers.
In labphew, this procedure is included in various method of the Operator class, for example
``analog_out`` which controls the voltage on the signal generator output,
or ``pps_out`` which sets the voltage of the programmable power supply.

View
^^^^

The view folder is the collection of interfaces for users to run an experiment. Different views can be written for the
same model, dependent on how the user likes to interact with the setup. A generic view can also work with different
models. A view module is usually initiated by calling an ``Operator`` to take care of the communication with devices
and the steps of the main control loop.
Views can be both working with command-line interface (CLI) or a graphical user interface (GUI).

An example of this is the ``BatteryTest_View.py`` which has been developed to implement various basic battery testing
functions.