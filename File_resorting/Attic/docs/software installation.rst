**************
How to Install
**************

Currently there is only one way to install the FAIR-Battery testing software, and that is from the source.
The most recent version of the project is stored on `this repository <https://github.com/SanliFaez/FAIR-Battery>`_.


Requirements
------------

The following software is required:

    - `Digilent Waveforms SDK <https://mautic.digilentinc.com/waveforms-download>`_
    - `git <https://github.com/git-guides/install-git#:~:text=To%20install%20Git%2C%20run%20the,installation%20by%20typing%3A%20git%20version%20.>`_
    - `python <https://www.python.org/downloads/>`_
    - `pip <https://pypi.org/project/pip/>`_

Installation from source
------------------------

Building the FAIR-Battery dependencies are tested on Windows and Mac PCs. It should be possible to install also on linux
but we have not tested it yet.

.. code::

    git clone https://github.com/SanliFaez/FAIR-Battery.git
    cd FAIR-Battery/
    pip install -r Battery_Testing_Software/requirements.txt

For a more in-depth step-by-step tutorial, see :doc:`FAIR-Battery 101`.

Getting started
---------------

Once you have installed FAIR-Battery successfully, you can test your installation by running the :doc:`FAIR-Battery 101` project.

If you want to start editing or adding to the code, we recommend that you fork the repository first to your own account
and install it from there. This way of installation allows you to stay connected with the FAIR-Battery repository and when
needed, rebase to future releases.



