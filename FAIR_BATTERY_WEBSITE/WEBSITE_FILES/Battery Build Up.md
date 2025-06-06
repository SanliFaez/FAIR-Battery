# Battery 101

## Flow batteries

Compared to traditional batteries, where the anodes, cathodes, separators and electrolyte are all contained within one structure (think of the popular AA Battery), flow batteries have their electrolyte in separate electrolyte tanks, outside of the of the reaction cell. Whereas in traditional batteries the electrolyte is contained, flow batteries actively pump the electrolyte through an ion-selective membrane. This has a few advantages, such as that the capacity of a flow battery is easily scalable, for one can just increase the tank size and the electro-active materials are easily recoverable.

Flow batteries are also stackable, where you can connect the two tanks to multiple cells to achieve a higher voltage.

Too learn more about flow batteries, their advantages and implementations, click [here](https://fbrc.dev/faq.html)!

## Architecture of the cell

![Battery_Schematic](Images/FullBatteryBluePrint.png){width="75%"}

**Fig. 1** A schematic example of a Redox Flow Battery. All components described in the legend can be found in every RFB. The V(V)/V(II) to V(IV)/V(III) redox reaction is used as an example.

### Electrolyte

The electrolyte in a redox-flow battery is the solution in the battery containing the chemical compounds which hold the (chemical) potential energy of the cell. This energy can be released when these compounds undergo a redox-reaction. Below an example is given of 2 half reactions which together add up to one redox reaction \[2\]\[4\].

| \# | Reaction | Δ*E* |
|----|----|---:|
| 1 | V<sup>3+</sup> + e<sup>-</sup> → V<sup>2+</sup> | \- 0.255 V vs. SHE |
| 2 | VO<sup>2+</sup> + H<sub>2</sub>O → VO<sub>2</sub><sup>+</sup> + 2 H<sup>+</sup> + e<sup>-</sup> | 1.004 V vs. SHE |
| 3 | V<sup>2+</sup> + 2 VO<sub>2</sub><sup>+</sup> + 4 H<sup>+</sup> → V<sup>3+</sup> + 2 VO<sup>2+</sup> + 2 H<sub>2</sub>O | 1.259 V |

**Table 1**

Reaction 1 and 2 are the half reactions after which the electric potential is given. Reaction 3 is the total reaction. The theoretical electric potential of reaction 3 is the difference in electric potential of the half reactions. One can see these energies are given in V, which is J/C.

### Membrane

Following the example of Table 1, if one would add V<sup>3+</sup> and VO<sup>2+</sup> into a solution without a membrane, the electron transfer of the oxidizer VO<sup>2+</sup> to the reducer V<sup>3+</sup> would happen at the side of the reaction. However, in an electrochemical battery, one controls the electron flow in order to use its energy. By putting putting a membrane between the solution containing the oxidizer and the solution containing the reducer, one doesn't allow the the oxidizer and reducer to be in direct contact. The electron transfer is happens via the so called electrodes (see Fig.1). In Fig. 1 at 5, a device can be added to be powered in case of discharge of the battery. In Fig.1 at 5, the charger can be located upon charging of the battery.\
The material of the membrane should be chosen to be non-reactive to the components in the of electrolyte and it should be permeable to the right components. One often used categorization for membranes is the distinction between anion- and cathion-exchanged membranes \[1\]. In general, cathion-exchanged membranes are used for high power density applications, while anion-exchanged membranes offer easier transport management and higher efficiency. Cathion and anion membranes can be categorized under ion exchange membranes, for they filter charged particles. Other types of membranes are porous seperators, bilayer membranes and asymmetric membranes \[3\].

### Current Collector

As briefly stated before, the current collector is the material at which the half reactions within the electrolyte take place. It can either offer or take up electrons. The current collector where the reduction reaction takes place is called the cathode. The current collector where the oxidation reaction takes place is called the anode. When charging the battery, the cathode is labeled as negative and the anode as positive. Upon discharge, the cathode becomes positive and the anode becomes negative. In Fig. 1, a discharging battery is shown. If the direction of current would be turn around, i.e. the battery would be charged, the labeling would be change by switching 1 and 2.\
To get back tot the example of the vanadium half reactions upon discharge of the cell; V<sup>3+</sup> + e<sup>-</sup> → V<sup>2+</sup> would take place on the cathode, while VO<sup>2+</sup> + H<sub>2</sub>O → VO<sub>2</sub><sup>+</sup> + 2 H<sup>+</sup> + e<sup>-</sup> takes place on the anode. A cell converting chemical energy to electric energy (discharging) is called a galvanic cell. A cell converting electric energy to chemical energy (charging) is called an electrolytic cell.\
The current collectors should sathisfy a few characteristics, depending on their specific use: - They should be inert to the electrolyte. This usually involves being inert to acidic environmemts. - They should be able to both offer and take up electrons to and from the electrolyte. - They should be low resistance - Ideally the should be porous to offer a large surface for the half reactions to take place.

### Current conductor

The current conductor is the part of the battery which conducts the current from the current collector to the other side of the cell. This can be the same material as the current collector, but could also be another material.\
The current conductor should sathisfy the following characteristics: - It have a low resistance - If the conductor is a different material than the current collector, there should be a good electron transmission between the material of the current collector and transmission

### The pump

The pump is located outside of the cell. The pump chooses the direction and speed of the electrlyte flow. The system contains one pump per halfcell.

## Properties of batteries and energy storage

In this section we will be discussing the properties of a functioning battery that can be used for energy storage. We will mainly be discussing some terms and properties that you will need in this project and that will effect battery performance.

### Overpotential

In an electrochemical battery undergoing a redox reaction, overpotential refers to the difference between the thermodynamically predicted voltage and the actual voltage measured under operating conditions.

When a battery is discharging and producing current, this results in a lower voltage than theoretically expected. Conversely, when charging a battery, more energy must be applied than the theoretical value to drive the reaction.

This occurs because a certain minimum voltage is required for electrolysis (interchange of electrons via the electrodes) to take place. The gap between this required voltage and the thermodynamically determined voltage is what defines the overpotential.

Overpotentail is directly linked to a batteries efficiency.

### Internal resistance

Although internal resistance is a somewhat generic term, as is only refers to a batteries natural predisposition to hinder current flow, we will discuss some of the sources that cause this hinder in flow.

The materials of which a battery is constructed greatly influence the internal resistance of the battery, as some materials are more conductive than other. Think for example of the conductivity of the electrolyte, separators or current collectors. These will all effect the resistance of the battery.

External factors also contribute. Temperature for example can influence the reaction rate, effecting the batteries performance.

## Test cell vs Battery

In this project, you will be constructing a test cell, but what exactly is the difference between a test cell and a battery, and why does that distinction matter?

A test cell in our case is essentially a simplified, experimental version of a battery. It is designed for research and development purposes, where access to internal components are essential.

Before a fully functioning and finalized battery can be manufactured, a test cell must be built and carefully studied. This stage is critical because it allows for modification and iteration. You can test different types of materials, and monitor how they influence the cell’s performance. When something does not work to your standard, you can easily access the responsible componants

The ability to evaluate these changes in a controlled and measurable way is what makes test cells so important. By gathering data from repeated trials, you can improve the design, enhance efficiency, and prevent future failures, all before committing to the manufacture of a complete battery system.

## Testing

When your test cell is build, you will have to perform some test to make sure it is working as expected. Here we will give a some things you will be working with.

1.  **Potentiostat**: A potentiastat is a device that allows you to measure.

## Bibliography

\[1\] Fumatech, https://www.fumatech.com/en/products/membranes-redox-flow-batteries/

\[2\] Molchanov, B. (2016). Development and testing of mechanically stable Vanadium redox flow battery.

\[3\] Gubler, L. (2019). Membranes and separators for redox flow batteries. Current Opinion in Electrochemistry, 18, 31-36.

\[4\] Choi, N. H., Kwon, S. K., & Kim, H. (2013). Analysis of the oxidation of the V (II) by dissolved oxygen using UV-visible spectrophotometry in a vanadium redox flow battery. Journal of the Electrochemical Society, 160(6), A973.

\[5\] Bobby (2014), https://blog.upsbatterycenter.com/overpotential-battery/

\[6\] Richard (2025), https://blog.upsbatterycenter.com/electrical-resistance-in-lithium-ion-batteries/

\[7\] Richard (2023), https://blog.upsbatterycenter.com/flow-battery-techology/
