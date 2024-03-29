# Charge-Discharge Testing
This protocol is meant to test the battery's' voltage as function of time and used capacity. This document is based on the section "Charge–discharge testing" in O'Connor, 2021 [1]. This experiment should generally be applicable for any redox-flow battery. However, the values for voltages and currents we use in this document consider the use of a vanadium redox-flow battery (VRFB).\

## Glossary
---
- **Negative tank** The tank containing the V(II)/V(III) solution (violet/green)
- **Positive tank** The tank containing the V(V)/V(IV) solution (yellow/blue). This solution might be black instead of colored.
- **V<sup>3.5</sup>** is a short way describe two electrolytes, one contains V(III) (no V(II)) and the other contains the same amount of V(IV) (no V(V)).
- **VRFB** Vanadium redox-flow battery

## Material
---
- VRFB
- (Optionally) Potentiostat
- Programmable power Supply  (*TTi QL335P linear regulated power*)

## Experiment
---
#### Making the battery anaerobe
When performing this experiment, the system should be kept anaerobe to prevent oxidation of formed V(II). This can be done by putting a humidified nitrogen or argon stream through the negative tank. Another option is to apply a film of paraffin oil on top of the electrolytes in the tanks [3]. This doesn't require you to supply the cell with constant nitrogen or argon stream. However, parts of the cell that are not airtight might still allow oxygen into the system, which won't be expelled when only using a paraffin oil and no nitrogen or argon stream.\
It is important to not make the entire battery airtight. In the cell hydrogen might be formed. If the entire battery is airtight, the battery can explode. We can enable the system to release overpressure using an overpressure valve.

#### Charge-discharge cycles
This experiment contains chronopotentiometry: charging and discharging the battery with constant current and with that measuring the voltage as a function of time. Upon charge the current should be positive, upon discharge the current will be negative.\
Based on the color of your electrolytes, it's possible to know the sign of the current you should start with. If your electrolytes are black/yellow and purple, then your battery is charged. This means you should start with a negative current. If your electrolytes are blue/black and green, it means your battery is discharged. In this case you should start with a positive current.\
The amount of current run through the battery cell is dependent on the size of your membrane. Use a 25 ml min<sup>-1</sup> flow rate of the electrolytes through the cell of  and keep this rate constant over the experiment. In [O'Connor, 2021] the current per area is ± 50 mA cm<sup>2</sup>.\
The charge-discharge cycles will cycle between 1.75 V (charging) and 1.10 V (discharging). When reaching these voltages, the direction of the current needs to be reversed.\

 These cycles can take quite some time. Best would be to have a tracking system, which can track the important quantities for you: voltage (V), time (s), current (A) and optionally capacity (A.h). A device which could track these values would be a computer controlled potentiostat, which can also perform the cycles. It might be possible that you do not own a potentiostat or your potentiostat can't reach the voltages required the perform these experiments. Performing one cycle by hand with a programmable power supply would suffice. However, the more cycles you track, the more you will know about your battery.\
 It is possible that the potentiostat or powersupply can't show the capacity. In that case, you can determine the capacity by integrating the absolute values current over time.
 You can plot the data as voltage and current versus time. Another way to show the data is to plot voltage versus capacity.\
 In the folder of this document, there will be a folder called "Script_plots". This folder contains a python script "Script_plots.py" which calculates the plot the data for you. There is an instruction file on how to use this script "Instructions_script.md".\
 In case you're using a potentiostat, make sure it can supply high enough currents and voltages. If it can, it will probably come accompanied by a software program which can generate the necessary data in plots for you.


## Possibility of black solution (instead of colored)
---
In our experiments we noticed that the electrolyte sometimes turned black. In our case this was the positive electrolyte. Our hypothesis is that this happens due to some of the electrode (carbon) being dispersed in the acidic electrolyte. The reason why this happens on the positive side and not the negative can be explained by looking at the half reactions happening upon charging:

|\# |Reaction | ΔE |
|-|--- | ---:|
|1| V<sup>3+</sup> +  e<sup>-</sup> &rarr; V<sup>2+</sup> | - 0.255 V vs. SHE|
|2| V(IV)O<sup>2+</sup> + H<sub>2</sub>O &rarr;  V(V)O<sub>2</sub><sup>+</sup> +  2 H<sup>+</sup> + e<sup>-</sup> |  1.004 V vs. SHE|

In reaction 1 there is no generation of H<sup>+</sup>. This half reaction corresponds to the negative electrolyte. Reaction 2 shows generation of 2 H<sup>+</sup>. This half reaction corresponds to the positive electrolyte. The generation of H<sup>+</sup> lowers the pH of the positive side the battery cell. This phenomenon in combination with high potentials on the electrode could lead to dissolvement of the electrode on the positive side. In case of proton blocking membrane, the pH of the negative electrolyte stays the same.   

## Bibliography
---
[1] O'Connor, H., Bailey, J. J., Istrate, O. M., Klusener, P. A., Watson, R., Glover, S., ... & Nockemann, P. (2022). An open-source platform for 3D-printed redox flow battery test cells. Sustainable Energy & Fuels, 6(6), 1529-1540.
[2] REFERENTIE OVER KLEUREN
[3] Wei, Z., Bhattarai, A., Zou, C., Meng, S., Lim, T. M., & Skyllas-Kazacos, M. (2018). Real-time monitoring of capacity loss for vanadium redox flow battery. Journal of Power Sources, 390, 261-269.
