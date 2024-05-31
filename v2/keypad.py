# keypad.py

import tkinter as tk
from tkinter import ttk

keypad_window = None

def open_keypad(root, freq_combobox=None, bw_combobox=None, ratio_combobox=None, power_combobox=None):
    global keypad_window
    if keypad_window is not None and keypad_window.winfo_exists():
        # If a keypad window is already open, bring it to the front
        keypad_window.lift()
        return

    keypad_window = tk.Toplevel(root)
    keypad_window.title("Keypad")
    keypad_window.geometry("350x350")  # Adjusted size of the keypad window
    keypad_window.attributes("-topmost", True)  # Keep the keypad window always on top

    # List of keypad buttons
    buttons = [
        '1', '2', '3',
        '4', '5', '6',
        '7', '8', '9',
        '.', '0', ':'
    ]

    # Options for the combobox
    options = ["Frequency", "Bandwidth", "Ratio", "Power"]
    selected_option = tk.StringVar(keypad_window)
    selected_option.set(options[0])  # Set default value

    # Set the width and padding for buttons and entries
    element_width = 8
    button_padx = 5
    button_pady = 5

    # Combobox for selecting the target input field
    combobox = ttk.Combobox(keypad_window, textvariable=selected_option, values=options, state='readonly', width=element_width)
    combobox.grid(row=0, column=0, columnspan=1, pady=(10, 30), padx=(10, 5), sticky=tk.EW)

    def on_button_click(button):
        current_text = command_entry.get()
        command_entry.delete(0, tk.END)
        command_entry.insert(tk.END, current_text + button)

    def confirm_value():
        value = command_entry.get()
        target = selected_option.get()
        if target == "Frequency" and freq_combobox:
            freq_combobox.delete(0, tk.END)
            freq_combobox.insert(tk.END, value)
        elif target == "Bandwidth" and bw_combobox:
            bw_combobox.delete(0, tk.END)
            bw_combobox.insert(tk.END, value)
        elif target == "Ratio" and ratio_combobox:
            ratio_combobox.delete(0, tk.END)
            ratio_combobox.insert(tk.END, value)
        elif target == "Power" and power_combobox:
            power_combobox.delete(0, tk.END)
            power_combobox.insert(tk.END, value)
        on_close()

    def on_close():
        global keypad_window
        keypad_window.destroy()
        keypad_window = None

    command_entry = ttk.Entry(keypad_window, width=element_width, font=('TkDefaultFont', 14), justify='center')
    command_entry.grid(row=0, column=1, columnspan=2, pady=(10, 30), padx=(5, 10), sticky=tk.EW)

    row_val = 2
    col_val = 0
    for button in buttons:
        action = lambda x=button: on_button_click(x)
        ttk.Button(keypad_window, text=button, command=action, width=element_width).grid(row=row_val, column=col_val, padx=button_padx, pady=button_pady, sticky=tk.EW)
        col_val += 1
        if col_val > 2:
            col_val = 0
            row_val += 1

    # Add a clear button
    ttk.Button(keypad_window, text="Clear", command=lambda: command_entry.delete(0, tk.END), width=element_width).grid(row=row_val, column=0, columnspan=1, padx=button_padx, pady=(20, 0), sticky=tk.EW)
    # Add a confirm button
    ttk.Button(keypad_window, text="Confirm", command=confirm_value, width=element_width).grid(row=row_val, column=1, columnspan=1, padx=button_padx, pady=(20, 0), sticky=tk.EW)
    # Add an exit button
    ttk.Button(keypad_window, text="Exit", command=on_close, width=element_width).grid(row=row_val, column=2, columnspan=1, padx=button_padx, pady=(20, 0), sticky=tk.EW)

    # Set the protocol for window close to handle the window tracking variable
    keypad_window.protocol("WM_DELETE_WINDOW", on_close)
