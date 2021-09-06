****************
FAIR-Battery 101 [WIP]
****************

As a "Hello World' this page will be going through the basic startup process, to get you up and running as
soon as possible. For a more details on installation see :doc:`software installation`.

Step 1: Installation
--------------------

Mac / Linux:
^^^^^^^^^^^^
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
versions) use them instead the version with a 3 for the rest of this guide.

Next complete the installation by running:

.. code::

    cd FAIR-Battery/Battery_Testing_Software
    pip3 install -r requirements_min.txt

If this completes successfully, you should be ready to open up some testing software:

.. code::

    export PYTHONPATH=.
    python3 labphew/view/design/BatteryTest_View.py  # todo: this isn't ready


Windows:
^^^^^^^^
You need to have `git <https://github.com/git-guides/install-git#:~:text=To%20install%20Git%2C%20run%20the,installation%20by%20typing%3A%20git%20version%20.>`_ installed first. Then in a terminal:

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
versions) use them instead the version with a 3 for the rest of this guide.

NOTE: If this isn't working after installation, perhaps python is not yet `added to path <https://www.c-sharpcorner.com/article/add-a-directory-to-path-environment-variable-in-windows-10/>`_.

Next complete the installation by running:
.. code::

    cd FAIR-Battery\Battery_Testing_Software
    pip3 install -r requirements_min.txt

If this completes successfully, you should be ready to run some testing software:

Windows:
The simplest method to run a python program in windows is to open the cloned repository with and IDE like PyCharm.
If you would rather do it in cmd, follow these instructions:

Add project to environment variables following `this guide <https://www.c-sharpcorner.com/article/add-a-directory-to-path-environment-variable-in-windows-10/>`_.
Instead of adding python to path though, we need to add the project to 'PYTHONPATH'



.. code::
    setx /m path "%pythonpath%;C:\parent\directory\of\project"
    python3 labphew/view/design/BatteryTest_View.py  # todo: this isn't ready