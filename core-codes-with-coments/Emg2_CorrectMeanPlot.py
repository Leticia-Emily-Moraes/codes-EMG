#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 16:58:09 2023

@author: kerberos
"""
#execfile ("Emg1_BurstAndPlot.py") #exec the first, but, paste below is the same
exec(open("Emg1_BurstAndPlot.py").read()) #This runs the first script (Emg1_BurstAndPlot.py) in the current namespace, making its variables like emg, time, etc. available.
# if using IPython: check variables from previous lesson are still in workspace
#whos

# process EMG signal: remove mean
emg_correctmean = emg - np.mean(emg) #Subtract the mean (average) of the EMG signal from the signal itself. This removes the DC offset (the constant 0.08 added in the simulation) and centers the signal around zero. This is a common preprocessing step in real EMG analysis.


# plot comparison of EMG with offset vs mean-corrected values
fig = plt.figure() #Create a new figure.
plt.subplot(1, 2, 1) #create a subplot grid with 1 row and 2 columns, and activate the first subplot (left).
plt.subplot(1, 2, 1).set_title('Mean offset present') #set title for the first subplot.
plt.plot(time, emg) #plot original EMG (with DC offset) vs time.
plt.locator_params(axis='x', nbins=4) #suggest that the x‑axis should have approximately 4 tick labels.
plt.locator_params(axis='y', nbins=4) #same for y‑axis.
plt.ylim(-1.5, 1.5) #set y‑axis limits from -1.5 to 1.5 to match both subplots for comparison.
plt.xlabel('Time (sec)') #x‑axis label.
plt.ylabel('EMG (a.u.)') #y‑axis label.

plt.subplot(1, 2, 2) #activate second subplot (right).
plt.subplot(1, 2, 2).set_title('Mean-corrected values') #title
plt.plot(time, emg_correctmean) #plot mean‑corrected EMG.
plt.locator_params(axis='x', nbins=4)  #suggest that the x‑axis should have approximately 4 tick labels.
plt.locator_params(axis='y', nbins=4) #same for y‑axis.
plt.ylim(-1.5, 1.5) #set y‑axis limits from -1.5 to 1.5 to match both subplots for comparison.
plt.xlabel('Time (sec)') #x‑axis label.
plt.ylabel('EMG (a.u.)') #y‑axis label.

fig.tight_layout() #Adjust subplot parameters to give specified padding and prevent overlap of labels.
fig_name = 'fig2.png' #Define filename (same as first script – will overwrite previous fig2.png).
fig.set_size_inches(w=11,h=7) #Set figure size to 11×7 inches.
fig.savefig(fig_name) #Save figure as PNG.