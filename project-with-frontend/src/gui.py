# src/gui.py
import tkinter as tk
from tkinter import messagebox, ttk, colorchooser
import threading
import os

import matplotlib.image as mpimg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Import the processing functions from the refactored module
from emg_functions import (
    generate_emg_signal,
    remove_mean_and_plot,
    filter_and_rectify,
    detect_onset_offset,
)

OUTPUT_DIR = "output_images"

# Maps the label shown in the combobox to the filter_type expected by emg_functions
FILTER_TYPES = {
    "Passa-baixa": "lowpass",
    "Passa-alta": "highpass",
    "Passa-banda": "bandpass",
    "Notch": "notch",
}


class EmgApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EMG Processing - Simulation and Filtering")
        self.root.geometry("340x500")
        self.root.resizable(False, False)

        # Variables used to store data between steps
        self.time_axis = None
        self.raw_emg_signal = None
        self.mean_corrected_emg = None
        self.filtered_emg = None
        self.rectified_emg = None
        self.onsets = None
        self.offsets = None

        # Filter settings (defaults match the original fixed 20-450 Hz band-pass)
        self.filter_type_var = tk.StringVar(value="Passa-banda")
        self.low_cutoff_var = tk.StringVar(value="20")
        self.high_cutoff_var = tk.StringVar(value="450")
        self.notch_freq_var = tk.StringVar(value="60")
        self.line_color = "tab:blue"

        # Flag to avoid multiple simultaneous processing tasks
        self.processing = False

        # Toplevel plot windows currently open, keyed by figure filename
        self.plot_windows = {}

        # Build the interface
        self.create_widgets()

    def create_widgets(self):
        # Main frame with padding
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Title
        lbl = tk.Label(main_frame, text="Choose a step:", font=("Arial", 11))
        lbl.pack(pady=(0, 15))

        # Large buttons arranged vertically
        self.btn_step1 = tk.Button(
            main_frame,
            text="1. Simulate and plot raw EMG",
            height=2,
            width=35,
            command=self.run_step1,
        )
        self.btn_step1.pack(pady=5)

        self.btn_step2 = tk.Button(
            main_frame,
            text="2. Remove mean (correct offset)",
            height=2,
            width=35,
            command=self.run_step2,
        )
        self.btn_step2.pack(pady=5)

        self.create_filter_settings(main_frame)

        self.btn_step3 = tk.Button(
            main_frame,
            text="3. Filter and rectify",
            height=2,
            width=35,
            command=self.run_step3,
        )
        self.btn_step3.pack(pady=5)

        self.btn_step4 = tk.Button(
            main_frame,
            text="4. Detect onset/offset",
            height=2,
            width=35,
            command=self.run_step4,
        )
        self.btn_step4.pack(pady=5)

    def create_filter_settings(self, parent):
        """Filter selection panel: filter type, cutoff/notch frequencies and line color.

        Changing any of these values while filtered data already exists (Button 3
        already run) re-applies the filter and refreshes the open figures right
        away, instead of requiring the user to click Button 3 again.
        """
        frame = tk.LabelFrame(parent, text="Filter settings", padx=10, pady=8)
        frame.pack(pady=5, fill=tk.X)

        row1 = tk.Frame(frame)
        row1.pack(fill=tk.X, pady=2)
        tk.Label(row1, text="Filter:", width=10, anchor="w").pack(side=tk.LEFT)
        self.filter_type_combo = ttk.Combobox(
            row1,
            textvariable=self.filter_type_var,
            values=list(FILTER_TYPES.keys()),
            state="readonly",
            width=15,
        )
        self.filter_type_combo.pack(side=tk.LEFT)
        self.filter_type_combo.bind("<<ComboboxSelected>>", self.on_filter_settings_changed)

        row2 = tk.Frame(frame)
        row2.pack(fill=tk.X, pady=2)
        tk.Label(row2, text="Low (Hz):", width=10, anchor="w").pack(side=tk.LEFT)
        self.low_cutoff_entry = tk.Entry(row2, textvariable=self.low_cutoff_var, width=8)
        self.low_cutoff_entry.pack(side=tk.LEFT)
        self.low_cutoff_entry.bind("<Return>", self.on_filter_settings_changed)
        self.low_cutoff_entry.bind("<FocusOut>", self.on_filter_settings_changed)

        tk.Label(row2, text="High (Hz):", width=10, anchor="w").pack(side=tk.LEFT, padx=(10, 0))
        self.high_cutoff_entry = tk.Entry(row2, textvariable=self.high_cutoff_var, width=8)
        self.high_cutoff_entry.pack(side=tk.LEFT)
        self.high_cutoff_entry.bind("<Return>", self.on_filter_settings_changed)
        self.high_cutoff_entry.bind("<FocusOut>", self.on_filter_settings_changed)

        row3 = tk.Frame(frame)
        row3.pack(fill=tk.X, pady=2)
        tk.Label(row3, text="Notch (Hz):", width=10, anchor="w").pack(side=tk.LEFT)
        self.notch_freq_entry = tk.Entry(row3, textvariable=self.notch_freq_var, width=8)
        self.notch_freq_entry.pack(side=tk.LEFT)
        self.notch_freq_entry.bind("<Return>", self.on_filter_settings_changed)
        self.notch_freq_entry.bind("<FocusOut>", self.on_filter_settings_changed)

        row4 = tk.Frame(frame)
        row4.pack(fill=tk.X, pady=(6, 0))
        tk.Label(row4, text="Color:", width=10, anchor="w").pack(side=tk.LEFT)
        self.color_swatch = tk.Label(
            row4, text="  ", bg=self.line_color, relief=tk.SUNKEN, width=4
        )
        self.color_swatch.pack(side=tk.LEFT)
        self.btn_color = tk.Button(row4, text="Change color", command=self.choose_color)
        self.btn_color.pack(side=tk.LEFT, padx=(10, 0))

        self.update_filter_fields_state()

    def update_filter_fields_state(self):
        """Enable/disable the cutoff/notch fields to match the selected filter type."""
        filter_type = FILTER_TYPES[self.filter_type_var.get()]
        low_state = tk.NORMAL if filter_type in ("highpass", "bandpass") else tk.DISABLED
        high_state = tk.NORMAL if filter_type in ("lowpass", "bandpass") else tk.DISABLED
        notch_state = tk.NORMAL if filter_type == "notch" else tk.DISABLED
        self.low_cutoff_entry.config(state=low_state)
        self.high_cutoff_entry.config(state=high_state)
        self.notch_freq_entry.config(state=notch_state)

    def choose_color(self):
        color = colorchooser.askcolor(color=self.line_color, title="Choose line color")
        if color[1] is not None:
            self.line_color = color[1]
            self.color_swatch.config(bg=self.line_color)
            self.on_filter_settings_changed()

    def get_filter_settings(self):
        """Reads and validates the current filter settings from the UI."""
        return {
            "filter_type": FILTER_TYPES[self.filter_type_var.get()],
            "low_cutoff": float(self.low_cutoff_var.get()),
            "high_cutoff": float(self.high_cutoff_var.get()),
            "notch_freq": float(self.notch_freq_var.get()),
            "line_color": self.line_color,
        }

    def on_filter_settings_changed(self, event=None):
        """Called whenever the filter type, cutoff/notch values or color change.

        Keeps the enabled fields in sync with the selected filter type, and if
        filtering has already been run once, re-applies it synchronously so the
        open figures reflect the new settings immediately.
        """
        self.update_filter_fields_state()
        if self.processing or self.mean_corrected_emg is None:
            return
        self.run_step3()

    # Helper methods for interface control
    def set_buttons_state(self, state):
        """Enable or disable all buttons."""
        self.btn_step1.config(state=state)
        self.btn_step2.config(state=state)
        self.btn_step3.config(state=state)
        self.btn_step4.config(state=state)

    def show_error(self, msg):
        """Display an error message (modal)."""
        messagebox.showerror("Warning", msg)

    # Launch tasks in threads
    def run_step1(self):
        if self.processing:
            return
        self.processing = True
        self.set_buttons_state(tk.DISABLED)
        threading.Thread(target=self._step1_thread, daemon=True).start()

    def _step1_thread(self):
        try:
            time_axis, raw_emg_signal = generate_emg_signal(output_dir=OUTPUT_DIR)
            self.time_axis = time_axis
            self.raw_emg_signal = raw_emg_signal
            # UI updates must be done on the main thread
            self.root.after(0, self._step1_done)
        except Exception as e:
            self.root.after(0, self._error_handler, f"Simulation error: {e}")

    def _step1_done(self):
        self.processing = False
        self.set_buttons_state(tk.NORMAL)
        messagebox.showinfo(
            "Completed", "Raw EMG signal generated and saved as 'fig2.png'."
        )
        # Show the figure in a new window
        self.show_plot_window("fig2.png")

    def run_step2(self):
        if self.processing:
            return
        # Check whether step 1 data exists
        if self.time_axis is None or self.raw_emg_signal is None:
            self.show_error("Run the simulation first (Button 1).")
            return
        self.processing = True
        self.set_buttons_state(tk.DISABLED)
        threading.Thread(target=self._step2_thread, daemon=True).start()

    def _step2_thread(self):
        try:
            time_axis, mean_corrected_emg = remove_mean_and_plot(
                self.time_axis, self.raw_emg_signal, output_dir=OUTPUT_DIR
            )
            self.mean_corrected_emg = mean_corrected_emg
            self.root.after(0, self._step2_done)
        except Exception as e:
            self.root.after(0, self._error_handler, f"Mean removal error: {e}")

    def _step2_done(self):
        self.processing = False
        self.set_buttons_state(tk.NORMAL)
        messagebox.showinfo("Completed", "Mean removed and figure 'fig2.png' updated.")
        self.show_plot_window("fig2.png")

    def run_step3(self):
        if self.processing:
            return
        # Check whether step 2 has been executed
        if self.time_axis is None or self.mean_corrected_emg is None:
            self.show_error("Run mean removal first (Button 2).")
            return
        try:
            filter_settings = self.get_filter_settings()
        except ValueError:
            self.show_error("Cutoff/notch frequencies must be numbers.")
            return
        self.processing = True
        self.set_buttons_state(tk.DISABLED)
        threading.Thread(
            target=self._step3_thread, args=(filter_settings,), daemon=True
        ).start()

    def _step3_thread(self, filter_settings):
        try:
            time_axis, filtered_emg, rectified_emg = filter_and_rectify(
                self.time_axis,
                self.mean_corrected_emg,
                output_dir=OUTPUT_DIR,
                **filter_settings,
            )
            self.filtered_emg = filtered_emg
            self.rectified_emg = rectified_emg
            self.root.after(0, self._step3_done)
        except Exception as e:
            self.root.after(0, self._error_handler, f"Filtering error: {e}")

    def _step3_done(self):
        self.processing = False
        self.set_buttons_state(tk.NORMAL)
        # Refresh already-open figures in place; open new windows only the first time
        self.show_plot_window("fig3.png")
        self.show_plot_window("fig4.png")

    def run_step4(self):
        if self.processing:
            return
        # Check whether step 3 has been executed
        if self.time_axis is None or self.rectified_emg is None:
            self.show_error("Run filtering and rectification first (Button 3).")
            return
        self.processing = True
        self.set_buttons_state(tk.DISABLED)
        threading.Thread(target=self._step4_thread, daemon=True).start()

    def _step4_thread(self):
        try:
            onsets, offsets, _ = detect_onset_offset(
                self.time_axis, self.rectified_emg, output_dir=OUTPUT_DIR
            )
            self.onsets = onsets
            self.offsets = offsets
            self.root.after(0, self._step4_done)
        except Exception as e:
            self.root.after(0, self._error_handler, f"Onset detection error: {e}")

    def _step4_done(self):
        self.processing = False
        self.set_buttons_state(tk.NORMAL)
        messagebox.showinfo(
            "Completed",
            f"Detected {len(self.onsets)} burst(s).\nFigure saved: 'fig5.png'.",
        )
        self.show_plot_window("fig5.png")

    def _error_handler(self, msg):
        self.processing = False
        self.set_buttons_state(tk.NORMAL)
        messagebox.showerror("Error", msg)

    # Display figures in a Toplevel window with a Matplotlib canvas
    def show_plot_window(self, filename):
        """Display the figure saved in the output directory.

        If a window for this filename is already open (e.g. a synchronous
        filter update), its image is refreshed in place instead of opening a
        duplicate window.
        """
        path = os.path.join(OUTPUT_DIR, filename)
        if not os.path.isfile(path):
            messagebox.showerror("Error", f"File not found: {path}")
            return

        existing = self.plot_windows.get(filename)
        if existing is not None:
            win, ax, canvas = existing
            ax.clear()
            ax.imshow(mpimg.imread(path))
            ax.axis("off")
            canvas.draw()
            win.lift()
            return

        # Create a new window
        plot_win = tk.Toplevel(self.root)
        plot_win.title(f"Figure: {filename}")
        plot_win.geometry("900x650")

        img = mpimg.imread(path)

        fig = Figure(figsize=(9, 6), dpi=100)
        ax = fig.add_subplot(111)
        ax.imshow(img)
        ax.axis("off")  # Remove axes because this is a raster image
        fig.tight_layout()

        # Embed the canvas in the window
        canvas = FigureCanvasTkAgg(fig, master=plot_win)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Add the navigation toolbar (zoom, pan, save)
        toolbar = NavigationToolbar2Tk(canvas, plot_win)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.plot_windows[filename] = (plot_win, ax, canvas)

        def on_close():
            del self.plot_windows[filename]
            plot_win.destroy()

        plot_win.protocol("WM_DELETE_WINDOW", on_close)

        # Button to close the window
        btn_close = tk.Button(plot_win, text="Close", command=on_close)
        btn_close.pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = EmgApp(root)
    root.mainloop()
