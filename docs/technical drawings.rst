******************
Technical Drawings  [WIP]
******************

**Battery Charging Circuit**
This circuit charges a battery using the AD2's programmable power supply (PPS).

.. image:: _static/Charge_Circuit.png
   :scale: 50 %
   :alt: Battery charging test circuit schematic

The charge current is read with the two
voltmeter channels of the AD2, 1+ and 2+. This allows us to get a differential voltage measurement across a known
resistance, and therefore calculate the current as simply:

.. math::

    I_{batt} = \frac{V_1-V_2}{R_{shunt}}