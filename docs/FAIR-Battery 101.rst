****************
FAIR-Battery 101 [WIP]
****************

As a "Hello World' this page will be going through the basic startup process, to get you up and running as
soon as possible. For a more details on installation see :doc:`software installation`.

Step 1: Installation
^^^^^^^^^^^^^^^^^^^
You need to have `git <https://github.com/git-guides/install-git#:~:text=To%20install%20Git%2C%20run%20the,installation%20by%20typing%3A%20git%20version%20.>`_ installed first. Then in a terminal:

.. code::
    cd parent/directory/for/project
    git clone https://github.com/SanliFaez/FAIR-Battery.git
    cd FAIR-Battery/Battery_Testing_Software

Next you need to have `python <https://pypi.org/project/pip/>`_ and `pip <https://pypi.org/project/pip/>`_ installed.
Verify this by running the following:

.. code::
    python3 --version
    pip3 --version

If all is well, these will both return a version number, otherwise please install them before continuing.

.. code::
    pip3 install -r requirements_min.txt
    export PYTHONPATH=.
    python3 labphew/view/design/BatteryTest_View.py  # todo: this isn't ready