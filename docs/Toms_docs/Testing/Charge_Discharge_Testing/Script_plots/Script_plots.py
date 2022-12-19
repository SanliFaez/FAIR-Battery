#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 11:13:03 2022

@author: tom


CAPACITY ACTS WEIRD AT THIS MOMENT
"""

import numpy as np
import matplotlib.pyplot as plt
"""
FILL IN 
"""

I = []
t = []
U = []

#%%


t_0 = t
dt = np.array(t_0) - np.roll(t_0,1)
Capacity = np.zeros(len(I))

for i in range(1,len(t)):
    Capacity[i] = Capacity[i-1] + I[i] * dt[i]
#%%

I = np.array(I)
t = np.array(t)
U = np.array(U)


#%%

fig,ax = plt.subplots()
ax.plot(t, U,'o', color = 'steelblue')
ax.plot(t, U, color = 'steelblue', label = 'Voltage')
ax.set_xlabel('$t$ (s)')
ax.set_ylabel('$U$ (V)', color = 'steelblue')


ax2 = ax.twinx()
ax2.plot(t, I, 'o', color = 'red')
ax2.plot(t, I, color = 'red', label = 'Current')
ax2.set_ylabel('$I$ (mA)', color = 'red')



plt.figure('Fig2')
plt.plot(Capacity, U)
plt.xlabel('$Capacity$ (mA.h)')
plt.ylabel('$U$ (V)')













