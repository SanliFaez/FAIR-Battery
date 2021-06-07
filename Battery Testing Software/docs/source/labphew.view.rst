***********
V for view
***********
All the files related to the GUI should be placed within the View package. This is the third leg of the
MVC design pattern. If the Model is properly built, the Views are relatively simple PyQt objects. It is
important to point out that if there is any logic of the experiment that goes into the view, the code is
going to become harder to share, unless it is for the exact same purpose.

The real-time plots are built on `pyQtGraph <http://www.pyqtgraph.org/>`_,
a GUI library that gives access to a powerful set of tools for embedding plots in user interfaces.

The icons used in the GUI are designed by `The Artificial <https://toicon.com>`_ and released under a CC-BY license.

The view is one of the most challenging aspects of any program,
since it requires a different set of skills compared to the rest of the program.
Building the view on top of a well-defined model makes it also independent from it.
By completely separating the logic of the experiment and the devices from the view itself,
it is possible to quickly prototype solutions that in most cases are enough for a researcher,
without getting lost in feature creep for the GUI.

Unless your measurement requires a very specific user-interaction that is essential for operating your setup or
your experiments, it is better to conform with the defaut GUI that comes with labphew.

There are two main GUIs implemented in labphew

``MonitorWindow``: is meant to stay active while the experiment is running. One can use this
interface to monitor the signals from the setup or make adjustments to the (physical) parameters.
Think of focusing on a certain imaging plane or adjusting the feedback parameters for a control loop.
Most of the operations that are required for safely starting and safely closing the connected devices
are also programmed in the ``MonitorWindow`` methods. One can easily change which signals are viewed.

One can also adjust the device or measurement parameters from the ``MonitorWindow`` which is effective done by
editing the corresponding `config.yml` file.

``ScanWindow``: can be called either from the ``MonitorWindow`` (inheriting the adjusted parameters throught the config file)
or from the command line (requires initializing the device connections, manually). The scan operations are measurement
sequences that are run with a fixed set of parameters and are meant to be saved for further processing.

It is relatively "easy" to define multiple scan operations and call them seprately from the ``MonitorWindow``.

Essential methods
-----------------

..
    .. automodule:: labphew.core.view_base.MonitorWindowBase
       :members:
       :undoc-members:
       :show-inheritance:

    .. automodule:: labphew.core.view_base.ScanWindowBase
       :members:
       :undoc-members:
       :show-inheritance:

    .. automodule:: labphew.core.view_base.general_worker
       :members:
       :undoc-members:
       :show-inheritance:
