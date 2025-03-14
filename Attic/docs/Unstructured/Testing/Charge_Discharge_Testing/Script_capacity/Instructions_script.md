# Instructions Script_capacity.py

## To open a python script:
1. Download anaconda here: https://www.anaconda.com/
2. Within anaconda, launch Spyder
3. Open the script Integration.py script within Spyder

## How to use the script:
1. There are 3 place which need to be filled in (under FILL IN in the script):
  - I, the current in mA
  - t, the time in s
  - U, the voltages in V

  As you can see in the script behind t and U there are brackets. You can fill all your measurements within the brackets. The iteration of your measurement needs to match the iteration in the bracket. Here is an example:\
  You have performed 3 measurements:
    1. *I* = 1250 A, *t* = 10 s, *U* = 1.40 V
    2. *I* = 1250 A, *t* = 100 s, *U* = 1.43 V
    3. *I* = 1250 A, *t* = 200 s, *U* = 1.44 V

  In the script, you would fill it in like this:\
  I = [1250, 1250, 1250]\
  t = [10, 100, 200]\
  U = [1.40, 1.43, 1.44]

2. Run the script. There is a button for this somewhere above, but you can also use the shortcut F5.

3. A plot is made of both voltage and current as a function of time. Also a plot is made of the voltage as a function of capacity.
