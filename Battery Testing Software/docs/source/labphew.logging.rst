*********************
Logging and debugging
*********************

It is recommended to make use of the default logging module of python.

Logging can be used to print statements to the screen and/or to a file.
Logging statements can be formatted to reveal useful information on where the message
comes from (e.g. the module, the class, the function, the linenumber) which is very helpful
as projects grow in size and complexity.
Logging statements can have different levels such as debug or warning
and by setting the overall logging level, one has control over which logging statements will
be printed and which will be hidden. This can is very useful during developing, to reduce or
increase the amount if information printed while running the code.
The commonly used levels are:

======== == ==================================================================================
DEBUG    10 Detailed information, typically of interest only when diagnosing problems.
INFO     20 Confirmation that things are working as expected.
WARNING  30 An indication that something unexpected happened, or indicative of some problem in the near future (e.g. 'disk space low'). The software is still working as expected.
ERROR    40 Due to a more serious problem, the software has not been able to perform some function.
CRITICAL 50 A serious error, indicating that the program itself may be unable to continue running.
======== == ==================================================================================

To use logging, the logging module needs to be imported and a logging object needs to be created
using the getLogger() function of the logging module.

.. code-block:: python

   import logging
   logging.basicConfig(level=logging.DEBUG)  # Change root logging level

   logger = logging.getLogger(__name__)      # Create logger object
   logger.setLevel(logging.INFO)             # Set the level of the logger

   logger.debug("Level INFO is higher than level DEBUG, so this will not be printed")
   logger.info("Here's some information for you")
   logger.warning("Something unexpected happened")
   logger.error("Oh no!")


It is a common practice to use the module name (i.e. __name__) as the name for the logger.
This helps in finding where the logging statement originated from.
The level of the logger can be modified using setLevel(). The level is a numeric value, but the logging
module has some handy shorthands like logging.INFO.
Note that the logging level of the logger object cannot be lower than the "root level" which
can be changed with logging.basicConfig().
More detailed information can be found in the official python logging documentation.
