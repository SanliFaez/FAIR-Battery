# Testing your battery cell

Now that you have build your cell, you will be able to test and access whether it is working properly. On this page we will provide the following tests you can perform:

1.  **First testing and charging of the battery**: Here you will test:

-   The charge/discharge-efficiency.
-   The overpotential as a function of current run through the battery. Knowing the relation between overpotential and current can tell you something about the internal resistance of the battery and the ideal current for best performance of the battery.
-   The terminal voltage as a function of time

2.  **Charge and discharge testing**: Here you will test the battery's' voltage as function of time and used capacity.
3.  **Stability electrode**: Here you will test the stability of current collectors and current conductors can be tested, based upon their resistance measured before and after exposure to the electrolyte.

The codes and complementary instructions for these experiments are provided below, where the numbering corresponds to the experiment with the same number given above:

1.  <div>

    -   [Intructions plot overpotential](./instructions_plot_overpotential.html)

    -   [Script plot overpotential](./Script_plot_overpotential.py)

    -   [Instructions charge discharge efficiency](./Instructions_charge_discharge_efficiency.html)

    -   [Script charge discharge efficiency](./Script_Charge_discharge_efficiency.py)

    </div>

2.  <div>

    -   [Instructions charge discharge script](./Instructions_script.html)

    -   [Script charge discharge plot](./Script_plots.py)

    </div>

## Software installation

To perform these tests, you will need the appropriate software to run all necessary programs. Follow the instructions below to proceed.

\* As a "Hello World' this page will be going through the basic startup process, to get you up and running as soon as possible. For general installation steps see :doc:`software installation`.

Warning: Not yet tried on linux, although the steps should be very similar to the "For Mac" section. \*

### For Mac

First you will need to install the waveforms SDK. It can be downloaded from the `Digilent site <https://mautic.digilentinc.com/waveforms-download>`\_.

NOTE: In the installer dragging the app to Applications is optional, but the "Waveforms SDK" MUST be added to your frameworks!

You need to have `git <https://github.com/git-guides/install-git#:~:text=To%20install%20Git%2C%20run%20the,installation%20by%20typing%3A%20git%20version%20.>`\_ installed first. Then in a terminal:

.. code::

```         
cd parent/directory/of/project
git clone https://github.com/SanliFaez/FAIR-Battery.git
```

Next you need to have `python <https://www.python.org/downloads/>`\_ and `pip <https://pypi.org/project/pip/>`\_ installed. Verify this by running the following:

.. code::

```         
python3 --version
pip3 --version
```

If all is well, these will both return a version number, otherwise please install them before continuing.

NOTE: If these don't work, try using "`python`" and "`pip`" instead. If these work (and show the correct latest versions) use them instead the version with a "3" for the rest of this guide.

Next complete the installation by running:

.. code::

```         
cd FAIR-Battery/
pip3 install -r Battery_Testing_Software/requirements.txt
```

If this completes successfully, you should be ready to open up some testing software.

First connect the usb of the AD2, then in path FAIR-Battery/ run:

.. code::

```         
export PYTHONPATH=.
python3 Battery_Testing_Software/examples/101_project/BatteryTest_View.py
```

### For Windows

First you will need to install the waveforms SDK. It can be downloaded from the `Digilent site <https://mautic.digilentinc.com/waveforms-download>`\_.

NOTE: In the installer choosing the app is optional, but the "Waveforms SDK" is mandatory!

Next you need to have `git <https://github.com/git-guides/install-git#:~:text=To%20install%20Git%2C%20run%20the,installation%20by%20typing%3A%20git%20version%20.>`\_ installed first. Then in CMD:

.. code::

```         
cd C:\parent\directory\of\project
git clone https://github.com/SanliFaez/FAIR-Battery.git
```

Next you need to have `python <https://www.python.org/downloads/>`\_ and `pip <https://pypi.org/project/pip/>`\_ installed.

Make sure to check the "Add Python #.# to PATH" option when installing!

Verify this by running the following:

.. code::

```         
python3 --version
pip3 --version
```

If all is well, these will both return a version number, otherwise please install them before continuing.

NOTE: If these don't work, try using "`python`" and "`pip`" instead. If these work (and show the correct latest versions) use them instead the version with a "3" for the rest of this guide.

NOTE: If this isn't working after installation, perhaps python is not yet `added to path <https://www.c-sharpcorner.com/article/add-a-directory-to-path-environment-variable-in-windows-10/>`\_.

Next complete the installation by running:

.. code::

```         
cd FAIR-Battery
pip3 install -r Battery_Testing_Software\requirements.txt
```
