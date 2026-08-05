#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 17:44:54 2023

@author: kerberos
"""
#import numpy as np – imports NumPy for numerical operations (random numbers, arrays).
#import matplotlib.pyplot as plt – imports Matplotlib for plotting.
# matplotlib inline – (commented) would display plots directly in Jupyter notebooks.

import numpy as np
import matplotlib.pyplot as plt
#matplotlib inline

# simulate EMG signal
burst1 = np.random.uniform(-1, 1, size=1000) + 0.08 #Generate 1000 random numbers uniformly distributed between -1 and 1, then add a constant 0.08 (DC offset). This simulates a burst of EMG activity.
burst2 = np.random.uniform(-1, 1, size=1000) + 0.08 #Same as burst1 – another 1000 samples with uniform noise + offset.
quiet = np.random.uniform(-0.05, 0.05, size=500) + 0.08 #Generate 500 samples of low‑amplitude uniform noise (range -0.05 to 0.05) plus the same offset 0.08. Represents muscle at rest (only noise).
emg = np.concatenate([quiet, burst1, quiet, burst2, quiet]) #Concatenate (join) the segments in order: 500 rest, 1000 burst, 500 rest, 1000 burst, 500 rest. Total length = 500+1000+500+1000+500 = 3500 samples.
time = np.array([i/1000 for i in range(0, len(emg), 1)]) # sampling rate 1000 Hz

# plot EMG signal
fig = plt.figure() #Create a new Matplotlib figure object.
plt.plot(time, emg) #Plot the EMG signal with time on x‑axis and amplitude on y‑axis.
plt.xlabel('Time (sec)') 
plt.ylabel('EMG (a.u.)') #Label the x‑axis as "Time (seconds)" and y‑axis as "EMG (a.u.)" where a.u. stands for arbitrary units (since the simulation does not have real physical units).
fig_name = 'fig2.png' #Define the filename for saving the plot.
fig.set_size_inches(w=11,h=7) #Set figure size to 11 inches wide and 7 inches tall.
fig.savefig(fig_name) #Save the figure as a PNG image file with the name 'fig2.png'.

