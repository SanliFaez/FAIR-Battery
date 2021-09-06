****************
FAIR-Battery 101
****************

As a "Hello World' this page will be going through the basic startup process, to get you up and running as
soon as possible. For a more details on installation see :doc:`software installation`.

Warning: Not yet tried on linux, although the steps should be very similar to the "For Mac" section.

For Mac
-------

First you will need to install the waveforms SDK. It can be downloaded from the `Digilent site <https://mautic.digilentinc.com/waveforms-download>`_.

NOTE: In the installer dragging the app to Applications is optional, but the "Waveforms SDK" MUST be added to your frameworks!

You need to have `git <https://github.com/git-guides/install-git#:~:text=To%20install%20Git%2C%20run%20the,installation%20by%20typing%3A%20git%20version%20.>`_ installed first. Then in a terminal:

.. code::

    cd parent/directory/of/project
    git clone https://github.com/SanliFaez/FAIR-Battery.git

Next you need to have `python <https://pypi.org/project/pip/>`_ and `pip <https://pypi.org/project/pip/>`_ installed.
Verify this by running the following:

.. code::

    python3 --version
    pip3 --version

If all is well, these will both return a version number, otherwise please install them before continuing.

NOTE: If these don't work, try using "``python``" and "``pip``" instead. If these work (and show the correct latest
versions) use them instead the version with a "3" for the rest of this guide.

Next complete the installation by running:

.. code::

    cd FAIR-Battery/
    pip3 install -r Battery_Testing_Software/requirements.txt

If this completes successfully, you should be ready to open up some testing software.

First connect the usb of the AD2, then in path FAIR-Battery/ run:

.. code::

    export PYTHONPATH=.
    python3 Battery_Testing_Software/examples/101_project/BatteryTest_View.py


For Windows
-----------

First you will need to install the waveforms SDK. It can be downloaded from the `Digilent site <https://mautic.digilentinc.com/waveforms-download>`_.

NOTE: In the installer choosing the app is optional, but the "Waveforms SDK" is mandatory!

Next you need to have `git <https://github.com/git-guides/install-git#:~:text=To%20install%20Git%2C%20run%20the,installation%20by%20typing%3A%20git%20version%20.>`_ installed first. Then in CMD:

.. code::

    cd C:\parent\directory\of\project
    git clone https://github.com/SanliFaez/FAIR-Battery.git

Next you need to have `python <https://pypi.org/project/pip/>`_ and `pip <https://pypi.org/project/pip/>`_ installed.

Make sure to check the "Add Python #.# to PATH" option when installing!

Verify this by running the following:

.. code::

    python3 --version
    pip3 --version

If all is well, these will both return a version number, otherwise please install them before continuing.

NOTE: If these don't work, try using "``python``" and "``pip``" instead. If these work (and show the correct latest
versions) use them instead the version with a "3" for the rest of this guide.

NOTE: If this isn't working after installation, perhaps python is not yet `added to path <https://www.c-sharpcorner.com/article/add-a-directory-to-path-environment-variable-in-windows-10/>`_.

Next complete the installation by running:

.. code::

    cd FAIR-Battery
    pip3 install -r Battery_Testing_Software\requirements.txt

If this completes successfully, you should be ready to open up some testing software.

First connect the usb of the AD2, then in path FAIR-Battery/ run:

.. code::

    set PYTHONPATH=%PYTHONPATH%;.
    python3 Battery_Testing_Software\examples\101_project\BatteryTest_View.py