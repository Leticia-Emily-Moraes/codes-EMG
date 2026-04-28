#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 17:44:54 2023

@author: kerberos
"""

import numpy as np
import matplotlib.pyplot as plt
#matplotlib inline

# simulate EMG signal
burst1 = np.random.uniform(-1, 1, size=1000) + 0.08
burst2 = np.random.uniform(-1, 1, size=1000) + 0.08
quiet = np.random.uniform(-0.05, 0.05, size=500) + 0.08
emg = np.concatenate([quiet, burst1, quiet, burst2, quiet])
time = np.array([i/1000 for i in range(0, len(emg), 1)]) # sampling rate 1000 Hz

# plot EMG signal
fig = plt.figure()
plt.plot(time, emg)
plt.xlabel('Time (sec)')
plt.ylabel('EMG (a.u.)')
fig_name = 'fig2.png'
fig.set_size_inches(w=11,h=7)
fig.savefig(fig_name)

