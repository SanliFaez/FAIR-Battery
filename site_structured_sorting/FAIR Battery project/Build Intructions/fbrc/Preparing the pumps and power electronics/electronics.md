---
Details:
    Thumbnail: images/test.jpg
    Time: Tens of minutes
    Difficulty: Easy
    Skills:
      - Electronics breadboarding
      - Flashing firmware to an Arduino 

---
<!-- There should be only one Header per page. You do not need to use all the keys -->
# Preparing the pumps and power electronics

{{BOM}}

## System overview

A [PC]{cat:tool, qty:1, Note:Must be able to flash firmware to microcontroller and connect over USB serial to microcontroller and potentiostat} communicates with both a charging/discharging device (typically a [potentiostat](pstat.md){cat:tool, qty:1, note: preferably the MYSTAT}) as well as an [Arduino UNO R3]{qty:1, Note:or equivalent microcontroller that can output two independent 5V PWM signals and connect to PC over USB serial}. These documents assume the use of a MYSTAT potentiostat and it's [modified control software](https://codeberg.org/FBRC/mystat/).

The Arduino is connected to an [L298N motor driver](drivers.md){cat:part, qty:1}, which is powered by a [24 V DC power source]{cat: part, qty: 1, Note: Anything between 12 V and 24 V may work but the results achieved here use 24 V. Motor speeds may need calibration to match existing results}. This is a simple dual H-bridge motor driver that allows the Arduino to control the speeds of the peristaltic pumps using pulse width modulation (PWM). There is no speed feedback; we only tell the motors which direction to turn and whether they run at 100% maximum speed, 0% speed (off), or anything in between. To know the speed (in rpm) or flowrate (in mL/min) of the peristaltic pumps, a separate measurement is required (like dispensing water into a graduated cylinder).

We use the open-source MYSTAT (with our own modifications to the control software), but any equivalent potentiostat or battery cycler will do. Our pump control system is based on the MYSTAT software, though, and can be used without the MYSTAT present.

With this hardware configuration, the MYSTAT software then allows for entire control of this electrochemical system: the applied currents and voltages as well as the speeds of the electrolyte pumps. 


## Flash firmware to microcontroller {pagestep}

Using the Arduino IDE with the elapsedMillis library installed, upload the following code to the Arduino. The location of the code in the repository is [here](https://codeberg.org/FBRC/RFB-dev-kit/src/branch/main/firmware/ArduinoUnoR3_MotorControl.ino)

## Remove on-board jumpers from motor driver {pagestep}

**Remove** the three on-board jumpers (highlighted in pink) from the motor driver board:

![](images/Screenshot_20240703_221706.png)

## Add Arduino and motor driver to the jig{pagestep}

There are standoffs made for the for the Arduino and motor driver on the back of the [jig](fromstep){qty: 1} .

## Add pumps to jig {pagestep}

Insert the two [peristaltic pumps with correct tubing](fromstep){qty:2} into their holders in the as shown:

![](images/Screenshot_20250102_190036.png)


## Connect cables between Arduino, motor driver, and power supply {pagestep}

Using [male-to-male breadboard jumper cables]{qty: several, cat: part} connect according to the below diagram, taking care to connect the negative terminal of the 24 V power supply lead to both the GND terminal of the motor driver (middle connection of the three-terminal screw connection header) **and** a GND pin of the Arduino, so that the Arduino's signals to the motor driver are in relation to the same fixed GND.
![](images/test.jpg)

Here is a proper schematic:

![](../CAD/exports/schematic.pdf)

The wiring should look like this when you're done (feel free to make it tidier!)
![](images/IMG_20241116_155825.jpg)

You now have a [jig with pumps and power electronics]{output, qty:1}.

## Connect microcontroller to PC and test pumps.

We are using the MYSTAT potentiostat and have modified the software to be able to control the pump speeds. If you have a different potentiostat, you can still use the MYSTAT software to control your pumps without having a MYSTAT connected.

Plug in the 24V power source to the H-bridge. Connect the Arduino to the PC with a [USB A-to-B cable]{qty: 1,cat: part}

Run the MYSTAT [modified control software](https://codeberg.org/FBRC/mystat/).

Connect to the Arduino through the MYSTAT GUI. Briefly test each pump to make sure it spins (it can spin for a couple seconds dry without issues).



