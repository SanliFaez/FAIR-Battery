***********
M for model
***********

Models are where all the logic of the ``Operator`` class should be placed.
In this case there are two models, one for the DAQ used and one for the Experiment itself.
Models rely on controllers to communicate with real devices and pass the information to the view in order to display it to the user.

Models do not only specify the overall logic of the experiment, they also specify how devices are used.
For example, if the camera is set to acquire one frame, to capture a movie one needs to run a sequence of
single-frame acquisitions.
The advantage of developing models for devices is that they offer common entry points to the user,
regardless of the underlying hardware.

The benefits of implementing models for devices may not seem obvious at the beginning,
but they become apparent for larger or long-term projects.
A common case found in many labs is the need for exchanging the hardware.
If the user upgrades or replaces part of the equipment, it is only needed to develop a new model,
and the rest of the code will continue to run, including the data acquisition, post-processing, analysis, etc.

Essential methods
-----------------