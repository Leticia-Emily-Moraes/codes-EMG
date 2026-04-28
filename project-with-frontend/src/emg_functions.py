# src/emg_functions.py
# Refactored functions from the original EMG processing scripts.
# The mathematical logic and output file names were preserved.

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal as sp_signal
import os


def generate_emg_signal(output_dir="output_images"):
    """
    Simulates the raw EMG signal (original Script 1).
    Saves 'fig2.png' with the raw signal.
    Returns: time (array), emg (array)
    """
    # Exact reproduction of the signal generation
    burst_segment_1 = np.random.uniform(-1, 1, size=1000) + 0.08
    burst_segment_2 = np.random.uniform(-1, 1, size=1000) + 0.08
    quiet_segment = np.random.uniform(-0.05, 0.05, size=500) + 0.08
    emg_signal = np.concatenate(
        [quiet_segment, burst_segment_1, quiet_segment, burst_segment_2, quiet_segment]
    )
    time_axis = np.array([i / 1000 for i in range(0, len(emg_signal), 1)])

    # Identical plotting and saving
    fig = plt.figure()
    plt.plot(time_axis, emg_signal)
    plt.xlabel("Time (sec)")
    plt.ylabel("EMG (a.u.)")
    os.makedirs(output_dir, exist_ok=True)
    fig_name = os.path.join(output_dir, "fig2.png")
    fig.set_size_inches(w=11, h=7)
    fig.savefig(fig_name)
    plt.close(fig)  # Close the figure to avoid unwanted display

    return time_axis, emg_signal


def remove_mean_and_plot(time_axis, emg_signal, output_dir="output_images"):
    """
    Removes the mean offset from the EMG signal (original Script 2).
    Saves 'fig2.png' (overwriting the previous one) with a comparison.
    Returns: time (array), emg_correctmean (array)
    """
    # Mean correction (identical)
    mean_corrected_emg = emg_signal - np.mean(emg_signal)

    # Comparison figure (subplots)
    fig = plt.figure()
    plt.subplot(1, 2, 1)
    plt.subplot(1, 2, 1).set_title("Mean offset present")
    plt.plot(time_axis, emg_signal)
    plt.locator_params(axis="x", nbins=4)
    plt.locator_params(axis="y", nbins=4)
    plt.ylim(-1.5, 1.5)
    plt.xlabel("Time (sec)")
    plt.ylabel("EMG (a.u.)")

    plt.subplot(1, 2, 2)
    plt.subplot(1, 2, 2).set_title("Mean-corrected values")
    plt.plot(time_axis, mean_corrected_emg)
    plt.locator_params(axis="x", nbins=4)
    plt.locator_params(axis="y", nbins=4)
    plt.ylim(-1.5, 1.5)
    plt.xlabel("Time (sec)")
    plt.ylabel("EMG (a.u.)")

    fig.tight_layout()
    os.makedirs(output_dir, exist_ok=True)
    fig_name = os.path.join(output_dir, "fig2.png")
    fig.set_size_inches(w=11, h=7)
    fig.savefig(fig_name)
    plt.close(fig)

    return time_axis, mean_corrected_emg


def filter_and_rectify(time_axis, mean_corrected_emg, output_dir="output_images"):
    """
    Butterworth band-pass filtering and rectification (original Script 3).
    Saves 'fig3.png' (filtered vs unfiltered) and 'fig4.png' (rectified vs unrectified).
    Returns: time, emg_filtered, emg_rectified
    """
    # Filter parameters (identical)
    high = 20 / (1000 / 2)
    low = 450 / (1000 / 2)
    b, a = sp_signal.butter(4, [high, low], btype="bandpass")

    # Filter application (filtfilt, identical)
    filtered_emg = sp_signal.filtfilt(b, a, mean_corrected_emg)

    # Figure 3 - before/after filter comparison
    fig = plt.figure()
    plt.subplot(1, 2, 1)
    plt.subplot(1, 2, 1).set_title("Unfiltered EMG")
    plt.plot(time_axis, mean_corrected_emg)
    plt.locator_params(axis="x", nbins=4)
    plt.locator_params(axis="y", nbins=4)
    plt.ylim(-1.5, 1.5)
    plt.xlabel("Time (sec)")
    plt.ylabel("EMG (a.u.)")

    plt.subplot(1, 2, 2)
    plt.subplot(1, 2, 2).set_title("Filtered EMG")
    plt.plot(time_axis, filtered_emg)
    plt.locator_params(axis="x", nbins=4)
    plt.locator_params(axis="y", nbins=4)
    plt.ylim(-1.5, 1.5)
    plt.xlabel("Time (sec)")
    plt.ylabel("EMG (a.u.)")

    fig.tight_layout()
    os.makedirs(output_dir, exist_ok=True)
    fig_name = os.path.join(output_dir, "fig3.png")
    fig.set_size_inches(w=11, h=7)
    fig.savefig(fig_name)
    plt.close(fig)

    # Rectification
    rectified_emg = abs(filtered_emg)

    # Figure 4 - rectified vs unrectified comparison
    fig = plt.figure()
    plt.subplot(1, 2, 1)
    plt.subplot(1, 2, 1).set_title("Unrectified EMG")
    plt.plot(time_axis, filtered_emg)
    plt.locator_params(axis="x", nbins=4)
    plt.locator_params(axis="y", nbins=4)
    plt.ylim(-1.5, 1.5)
    plt.xlabel("Time (sec)")
    plt.ylabel("EMG (a.u.)")

    plt.subplot(1, 2, 2)
    plt.subplot(1, 2, 2).set_title("Rectified EMG")
    plt.plot(time_axis, rectified_emg)
    plt.locator_params(axis="x", nbins=4)
    plt.locator_params(axis="y", nbins=4)
    plt.ylim(-1.5, 1.5)
    plt.xlabel("Time (sec)")
    plt.ylabel("EMG (a.u.)")

    fig.tight_layout()
    fig_name = os.path.join(output_dir, "fig4.png")
    fig.set_size_inches(w=11, h=7)
    fig.savefig(fig_name)
    plt.close(fig)

    return time_axis, filtered_emg, rectified_emg
