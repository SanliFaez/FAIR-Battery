#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 12:30:09 2022

@author: tom
"""

import matplotlib.pyplot as plt
import numpy as np

"FILL IN"
I = []
U = []
I_unit = "mA"
V_unit = "V"


#%%
plt.figure()
plt.plot(I, U,'o')
plt.plot(I, U, '--')
plt.xlabel('$I$ ('+I_unit+')')
plt.ylabel('$U$ ('+V_unit+')')



#legend = plt.legend(loc='best', fontsize='medium')