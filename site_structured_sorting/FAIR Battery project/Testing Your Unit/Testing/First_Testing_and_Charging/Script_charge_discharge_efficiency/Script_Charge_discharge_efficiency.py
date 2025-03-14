#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 09:23:02 2022

@author: tom
"""

import numpy as np
import matplotlib.pyplot as plt
"""
FILL IN 
"""

x_charge = []
t_charge = []
a_charge = []

x_discharge = [] 
t_discharge = []
a_discharge = []

#%%
def E(x,t,a):
    x = [0] + x
    t = [0] + t
    a = [1] + list(a)
    x_1 = np.array(a) * np.array(x)
    dt = np.array(t) - np.roll(t,1)
    return np.sum(x_1[1:]*dt[1:])

E_charge = E(x_charge, t_charge, a_charge)
E_discharge = E(x_discharge, t_discharge, a_discharge)


efficiency = E_discharge/E_charge

print("Charge/discharge efficiency = ", efficiency)
plt.plot(x_charge, t_charge, label = 'Charge')
plt.plot(x_discharge, t_discharge, label = 'Discharge')
legend = plt.legend(loc='best', fontsize='medium')



