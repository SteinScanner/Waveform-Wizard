import numpy as np
from scipy.io.wavfile import write
import tkinter as tk
from tkinter import ttk, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def create_oscilloscope_waveform(filename, shape_function, duration=2.0, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    # generate the waveforms
    x, y = shape_function(t)
    
    # normalize to the range [-1, 1]
    x /= np.max(np.abs(x))
    y /= np.max(np.abs(y))
    
    # convert to 16-bit PCM audio
    x = np.int16(x * 32767)
    y = np.int16(y * 32767)
    
    # combine the left and right
    stereo_waveform = np.column_stack((x, y))
    
    # write a .wav file
    write(filename, sample_rate, stereo_waveform)

def circle_shape(t, frequency=1.0):
    x = np.cos(2 * np.pi * frequency * t)
    y = np.sin(2 * np.pi * frequency * t)
    return x, y

def lissajous_shape(t, a=3, b=2, delta=np.pi / 2):
    x = np.sin(a * t + delta)
    y = np.sin(b * t)
    return x, y

def figure_eight_shape(t, frequency=1.0):
    x = np.sin(2 * np.pi * frequency * t)
    y = np.sin(4 * np.pi * frequency * t)
    return x, y

def spiral_shape(t, frequency=1.0):
    x = t * np.cos(2 * np.pi * frequency * t)
    y = t * np.sin(2 * np.pi * frequency * t)
    return x, y

def update_preview(canvas, ax, shape_function, duration):
    t = np.linspace(0, duration, 1000)
    x, y = shape_function(t)
    ax.clear()
    ax.plot(x, y)
    ax.set_aspect('equal')
    ax.axis('off')
    canvas.draw()

def save_waveform(shape_name, duration):
    shape_functions = {
        'Circle': circle_shape,
        'Lissajous': lissajous_shape,
        'Figure Eight': figure_eight_shape,
        'Spiral': spiral_shape
    }
    
    shape_function = shape_functions[shape_name]
    
    # where to save
    filename = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
    if filename:
        create_oscilloscope_waveform(filename, shape_function, duration=duration)
        tk.messagebox.showinfo("Success", f"{shape_name} waveform saved as {filename}")

def on_shape_selected(event, canvas, ax, shape_var, duration_var):
    shape_functions = {
        'Circle': circle_shape,
        'Lissajous': lissajous_shape,
        'Figure Eight': figure_eight_shape,
        'Spiral': spiral_shape
    }
    
    shape_function = shape_functions[shape_var.get()]
    duration = float(duration_var.get())
    update_preview(canvas, ax, shape_function, duration)

def on_duration_changed(event, canvas, ax, shape_var, duration_var):
    on_shape_selected(event, canvas, ax, shape_var, duration_var)

def main():
    root = tk.Tk()
    root.title("Oscilloscope Waveform Generator")
    
    # add label for shape selection
    label = ttk.Label(root, text="Select a Shape to Generate:")
    label.pack(pady=10)
    
    # add combobox for shape selection
    shape_var = tk.StringVar()
    shape_combobox = ttk.Combobox(root, textvariable=shape_var)
    shape_combobox['values'] = ('Circle', 'Lissajous', 'Figure Eight', 'Spiral')
    shape_combobox.current(0)  # Set default to 'Circle'
    shape_combobox.pack(pady=10)
    
    # label for duration selection
    duration_label = ttk.Label(root, text="Select Duration (seconds):")
    duration_label.pack(pady=10)
    
    # slider for duration selection
    duration_var = tk.DoubleVar(value=2.0)
    duration_slider = ttk.Scale(root, from_=0.5, to=10.0, variable=duration_var, orient=tk.HORIZONTAL)
    duration_slider.pack(pady=10)
    
    # add a matplotlib figure for preview
    fig, ax = plt.subplots(figsize=(4, 4))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(pady=10)
    
    # initial preview
    update_preview(canvas, ax, circle_shape, duration_var.get())
    
    # update the preview
    shape_combobox.bind("<<ComboboxSelected>>", lambda event: on_shape_selected(event, canvas, ax, shape_var, duration_var))
    duration_slider.bind("<Motion>", lambda event: on_duration_changed(event, canvas, ax, shape_var, duration_var))
    
    # save button
    save_button = ttk.Button(root, text="Save Waveform", command=lambda: save_waveform(shape_var.get(), duration_var.get()))
    save_button.pack(pady=10)
    
    # GUI loop
    root.mainloop()

if __name__ == "__main__":
    main()
