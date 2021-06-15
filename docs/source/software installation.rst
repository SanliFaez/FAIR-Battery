**************
How to install [WIP]
**************

Stable versions of labphew are uploaded on PyPI. The easiest way to get this versions is via

    pip install labphew

The most recent version of labphew is stored on `this repository <https://github.com/sanlifaez/labphew>`_.
Since labphew is not supposed to be a supporing package, but an educational framework, there is a good chance that
you might need to edit the code. Therefore, forking this repo into your own working environment will probably
be handy at some point.

They are two recommended ways of installing labphew and using it out of the box:

Installation from the Python package index
------------------------------------------
You need to have `pip <https://pypi.org/project/pip/>`_ installed.

If affirmative, from the command line you can use:

.. code::

    pip install labphew

Installation from source
------------------------

Building the labphew dependencies are tested on Windows and Mac PCs. It should be possible to install also on linux but we have not tested it yet.

.. code::

    git clone https://github.com/sanlifaez/labphew.git
    cd labphew
    pip install .

If you want to start editing or adding to the code, we recommend that you fork the repository first to your own account and install it from there. This way of installation allows you to stay connected with the  labphew repository and when needed, rebase to future releases.

Getting started
---------------

Once you have installed labphew, successfully, you can test your installation by using the following from the command line

.. code::
    labphew start blink -d

You can expect a labphew window with with you can interact. To go further,
you can consider checking the :doc:`./walkthrough`.


