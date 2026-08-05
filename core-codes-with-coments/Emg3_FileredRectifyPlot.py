#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 17:20:48 2023

@author: kerberos
"""
exec(open("Emg2_CorrectMeanPlot.py").read()) #Runs the second script (which itself runs the first script) so that variables emg_correctmean and time become available in the current workspace. This is a chained execution.

import scipy as sp #imports SciPy, a library for scientific computing.
from scipy import signal #imports the signal submodule directly (can also use sp.signal). Actually, after import scipy as sp, you can already use sp.signal. This second line is redundant but harmless.

# create bandpass filter for EMG
high = 20/(1000/2) #Normalizes the lower cutoff frequency (20 Hz) by the Nyquist frequency. Nyquist frequency = sampling_rate/2 = 1000/2 = 500 Hz. Result: 20/500 = 0.04.
low = 450/(1000/2) #Normalizes the upper cutoff frequency (450 Hz): 450/500 = 0.9.
b, a = sp.signal.butter(4, [high,low], btype='bandpass') #Designs a 4th order Butterworth bandpass filter with passband between 20 Hz and 450 Hz. Returns numerator coefficients b and denominator coefficients a (for an IIR filter).

# process EMG signal: filter EMG
emg_filtered = sp.signal.filtfilt(b, a, emg_correctmean) #applies the filter forward and backward to eliminate phase shift (zero-phase filtering). This is important for EMG analysis because it preserves the timing of events. Input: coefficients b, a and the mean-corrected EMG signal.

# plot comparison of unfiltered vs filtered mean-corrected EMG
fig = plt.figure()
plt.subplot(1, 2, 1)
plt.subplot(1, 2, 1).set_title('Unfiltered EMG')
plt.plot(time, emg_correctmean)
plt.locator_params(axis='x', nbins=4)
plt.locator_params(axis='y', nbins=4)
plt.ylim(-1.5, 1.5)
plt.xlabel('Time (sec)')
plt.ylabel('EMG (a.u.)')

plt.subplot(1, 2, 2)
plt.subplot(1, 2, 2).set_title('Filtered EMG')
plt.plot(time, emg_filtered)
plt.locator_params(axis='x', nbins=4)
plt.locator_params(axis='y', nbins=4)
plt.ylim(-1.5, 1.5)
plt.xlabel('Time (sec)')
plt.ylabel('EMG (a.u.)')

fig.tight_layout()
fig_name = 'fig3.png'
fig.set_size_inches(w=11,h=7)
fig.savefig(fig_name) #Creates a figure with two subplots side by side. Left: mean‑corrected but unfiltered EMG. Right: bandpass‑filtered EMG. Both share the same y‑axis limits (-1.5 to 1.5) for fair comparison. Saves as fig3.png

# process EMG signal: rectify
emg_rectified = abs(emg_filtered) #Takes the absolute value of the filtered EMG signal. This is called full‑wave rectification. It flips all negative values to positive, creating a signal that represents the envelope of the muscle activity. Rectification is a common step before extracting features like mean absolute value or RMS.

# plot comparison of unrectified vs rectified EMG
fig = plt.figure()
plt.subplot(1, 2, 1)
plt.subplot(1, 2, 1).set_title('Unrectified EMG')
plt.plot(time, emg_filtered)
plt.locator_params(axis='x', nbins=4)
plt.locator_params(axis='y', nbins=4)
plt.ylim(-1.5, 1.5)
plt.xlabel('Time (sec)')
plt.ylabel('EMG (a.u.)')

plt.subplot(1, 2, 2)
plt.subplot(1, 2, 2).set_title('Rectified EMG')
plt.plot(time, emg_rectified)
plt.locator_params(axis='x', nbins=4)
plt.locator_params(axis='y', nbins=4)
plt.ylim(-1.5, 1.5)
plt.xlabel('Time (sec)')
plt.ylabel('EMG (a.u.)')

fig.tight_layout()
fig_name = 'fig4.png'
fig.set_size_inches(w=11,h=7)
fig.savefig(fig_name) #Another comparison figure: left shows filtered but unrectified EMG (still bipolar), right shows rectified EMG (all positive). Same axis limits. Saves as fig4.png. Note that after rectification, the signal is still oscillatory (not smoothed). Often one would then apply a low‑pass filter to obtain a linear envelope.