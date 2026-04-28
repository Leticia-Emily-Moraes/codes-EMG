# src/gui.py
import tkinter as tk
from tkinter import messagebox
import threading
import os

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Import the processing functions from the refactored module
from emg_functions import generate_emg_signal, remove_mean_and_plot, filter_and_rectify

OUTPUT_DIR = "output_images"


class EmgApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EMG Processing - Simulation and Filtering")
        self.root.geometry("320x240")
        self.root.resizable(False, False)

        # Variables used to store data between steps
        self.time_axis = None
        self.raw_emg_signal = None
        self.mean_corrected_emg = None
        self.filtered_emg = None
        self.rectified_emg = None

        # Flag to avoid multiple simultaneous processing tasks
        self.processing = False

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

        self.btn_step3 = tk.Button(
            main_frame,
            text="3. Filter and rectify",
            height=2,
            width=35,
            command=self.run_step3,
        )
        self.btn_step3.pack(pady=5)

    # Helper methods for interface control
    def set_buttons_state(self, state):
        """Enable or disable all buttons."""
        self.btn_step1.config(state=state)
        self.btn_step2.config(state=state)
        self.btn_step3.config(state=state)

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
        self.processing = True
        self.set_buttons_state(tk.DISABLED)
        threading.Thread(target=self._step3_thread, daemon=True).start()

    def _step3_thread(self):
        try:
            time_axis, filtered_emg, rectified_emg = filter_and_rectify(
                self.time_axis, self.mean_corrected_emg, output_dir=OUTPUT_DIR
            )
            self.filtered_emg = filtered_emg
            self.rectified_emg = rectified_emg
            self.root.after(0, self._step3_done)
        except Exception as e:
            self.root.after(0, self._error_handler, f"Filtering error: {e}")

    def _step3_done(self):
        self.processing = False
        self.set_buttons_state(tk.NORMAL)
        messagebox.showinfo(
            "Completed",
            "Filtering and rectification completed.\n"
            "Figures saved: 'fig3.png' and 'fig4.png'.",
        )
        # Show two figures in separate windows (or they could be combined)
        self.show_plot_window("fig3.png")
        self.show_plot_window("fig4.png")

    def _error_handler(self, msg):
        self.processing = False
        self.set_buttons_state(tk.NORMAL)
        messagebox.showerror("Error", msg)

    # Display figures in a Toplevel window with a Matplotlib canvas
    def show_plot_window(self, filename):
        """Display the figure saved in the output directory in a new window."""
        path = os.path.join(OUTPUT_DIR, filename)
        if not os.path.isfile(path):
            messagebox.showerror("Error", f"File not found: {path}")
            return

        # Create a new window
        plot_win = tk.Toplevel(self.root)
        plot_win.title(f"Figure: {filename}")
        plot_win.geometry("900x650")

        # Load the image into a Matplotlib Figure so it can be redrawn with full control
        import matplotlib.image as mpimg

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

        # Button to close the window
        btn_close = tk.Button(plot_win, text="Close", command=plot_win.destroy)
        btn_close.pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = EmgApp(root)
    root.mainloop()
