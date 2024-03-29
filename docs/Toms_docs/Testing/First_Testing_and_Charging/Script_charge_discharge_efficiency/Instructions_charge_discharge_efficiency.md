# Instructions Charge_discharge_efficiency.py

## To open a python script:
1. Download anaconda here: https://www.anaconda.com/
2. Within anaconda, launch Spyder
3. Open the script Integration.py script within Spyder

## How to use the script:
1. There are 5 place which need to be filled in (under FILL IN in the script):

	- **x** = your variable. For instance if you chose to vary the current and keep the voltage constant,
	then x is the current. If you chose to keep the current constant and vary the voltage,
	then x is your voltage. x_charge means your measurements upon charging,
	x_discharge is for your measurements upon discharge.

	- **t** = is the time at which you measured x.

	notice that in the script for x and t the =-sign is followed by brackets ([]). You need to fill in your measured data within those brackets and seperate them with comma's. It is also important the data of x, t and a is alligned. For instance. if you measured at charging *I*(*t*) = 10 mA, 12 mA and 16 mA respectively at *t* = 0 s, 60 s and 90 s with V = 0.3 V, 0.3 V, 0.4 V. Then you need to fill this in the script as x_charge = [10, 12, 16] and t_charge = [0,60,90], a = [0.3 V, 0.3 V, 0.4 V].

	- **a** = 1 if your variable is the power. In that case, you can write down np.ones(n), where n is the number of measurements you have done. If your measuring current and voltage, a is the quantity that follows the varied quantity. For instance, if you're varying the current while keeping voltage constant, **a** is the voltage.
	If you're measuring *U* and *I* for charging of the battery, **a** will also vary per measurements. At discharge **a** will be constant. For discharge you can use **a** = a0 * np.ones(n), where a0 is the value of the quantity a.

2. Run the script. There is a button for this somewhere above, but you can also use the shortcut F5.

3. The charge/discharge efficiency is printed in your console. If everything works fine, also a plot of your variable as function of time to check if you haven't made a mistake with filling in the measured quantities.
