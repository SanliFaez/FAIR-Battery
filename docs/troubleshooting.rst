***************
Troubleshooting  [WIP]
***************

Is something not working right? Hopefully the steps below will help you get your battery up and running again, otherwise
please submit an issue. See LINK for more information on how to submit an issue and what to include.

Hardware Troubleshooting
------------------------

**Troubleshooting Steps:**

    1. Turn it off and on
    2. Check the connections
    3. Check the voltage test points

Software Troubleshooting
------------------------
Simple troubleshooting can be done by reading the popup errors that the Battery Testing software provides. More
sophisticated issue however may require you to read the errors that appear in the terminal window of your code editor.

**Error: Module Not Found**
^^^^^^^^^^^^^^^^^^^^^^^^^^^
This occurs when your python project path variable has not been set.
To fix this open a terminal and navigate to the project root directory:

.. code::

    cd FAIR-Battery/

Next set the path to the current directory.

Mac / Linux:

.. code::

    export PYTHONPATH=.

Mac / Linux:

.. code::

    set PYTHONPATH=%PYTHONPATH%;.


**Error: AD2 Device not connected**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Check the USB connection to the Analog Discovery 2 board. Try various USB cables in case one has broken or does not have
data lines. Perhaps also try the same USB cable with another device that requires data lines, to make sure this isn't
the issue.