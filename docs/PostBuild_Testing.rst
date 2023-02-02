Post-build Testing
====================

After building the cell it is important to first check if the battery
leakage-free. Pump demi water for half an hour through the cell.
By putting something like a paper towel under the cell. Any leaked water
will then be visible.
If the cell is leakage free, the first test on it can be performed.

Battery Spectroscopy
-----------------------------------------
One can learn about the impedance of a battery by performing
battery spectroscopy. Impedance can be seen as an AC analog
for the DC relevant quantity; resistance. The impedance *Z* can
be calculated using the following equation:

==================================================    ===========
:math:`Z = (\frac{|U|}{|I|})e^{i\omega t+ \phi}`          equation 1
==================================================    ===========

Where l *U* l is that absolute value of voltage in V,
l *I* l is the absolute current in A, *ω* is the AC frequency
in Hz and *φ* is a phase-difference between *U* and *I*.
From the equation, you can see the impedance has a complex
value.
There are 2 relevant figures one can make
to learn about the impedance within the battery:

-   **Bode plot:** this shows either the real or imaginary
    part of on the vertical axis and the frequency of AC on
    the horizontal axis. Below, an example is shown:
.. figure:: /BodePlot_Example.png

    **Fig. 1** The different colours of the plot represent different measurements.


-   **Nyquist plot:** this image shows the imaginary part
    of the impedance on the vertical axis and the real part
    on the horizontal axis. Below, an example is shown:
.. figure:: /NyquistPlot_Example.png

    **Fig. 2** The different colours of the plot represent different measurements.

It is possible to make these plots using a programmable
potentiostat with the right software. We use a PalmSens EmStat4S
with complementary software PSTrace 5.
A potentiostat has 5 wires which can be connected to the battery:
Do as follows:

-   Connect the **Working Electrode** to the V(IV)/V(V) side
-   Connect the **Sense Electrode** to the V(IV)/V(V) side
-   Connect the **Reference Electrode** to the V(II)/V(III) side
-   Connect the **Counter Electrode** to the V(II)/V(III) side
-   Don't connect the **Grounding Electrode**

Make sure when measuring to generate a flow of the electrolyte
trough the cell.
Using PSTrace 5, it is possible to generate a Bode en Nyquist
plot.