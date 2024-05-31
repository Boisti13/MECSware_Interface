import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import json
from utilities import clear_console, show_waiting_message

# Global variables to store the retrieved values
frequency_value = ""
bandwidth_value = ""
power_value = ""

def setup_event_handlers(root, frame):
    root.bind("<Button-1>", lambda event: close_open_lists(event, frame))

def close_open_lists(event, frame):
    for child in frame.winfo_children():
        if isinstance(child, tk.Frame):
            child.place_forget()

def ping_command():
    """Function to start the ping test in a separate thread."""
    threading.Thread(target=ping_test).start()

def ping_test():
    """Function to execute a ping test to the provided IP address."""
    try:
        # Retrieve the IP address from the input field
        ip_address = ip_entry.get()
        clear_console()
        # Run the ping command
        result = subprocess.run(['ping', '-c', '1', ip_address], capture_output=True, text=True)
        output_text.insert(tk.END, result.stdout)

        # Show the ping result in a messagebox
        if result.returncode == 0:
            messagebox.showinfo("Ping Result", "Ping successful!")
        else:
            messagebox.showerror("Ping Result", "Ping failed!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def get_current_data():
    """Function to get the current data from the server."""
    global frequency_value, bandwidth_value, power_value

    try:
        # Retrieve values from the input fields
        ip_address = ip_entry.get()
        port = port_entry.get()
        name = name_entry.get()

        # Construct the command to be executed
        command = (
            f"curl -X GET https://{ip_address}:{port}/5g/bs/status/{name} -k -u admin:admin "
            f"-H \"Content-Type: application/json\" -v"
        )

        show_waiting_message()
        # Run the command in a subprocess
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout

        # Update the output text widget with the result
        output_text.after(0, output_text.delete, "end-2l", "end-1l")
        output_text.after(0, output_text.insert, tk.END, output)

        # Parse the JSON response
        data = json.loads(output)
        frequency_value = data.get("frequency", "")
        bandwidth_value = data.get("bandwidth", "")
        power_value = data.get("tx_power", "")

        # Update the labels with the current data
        frequency_label.config(text=f"{frequency_value}")
        bandwidth_label.config(text=f"{bandwidth_value}")
        power_label.config(text=f"{power_value}")

        messagebox.showinfo("Current Data", f"Frequency: {frequency_value}\nBandwidth: {bandwidth_value}\nPower: {power_value}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def submit_command():
    """Function to submit a command and show a confirmation message."""
    trigger_terminal_command_submit_data()
    messagebox.showinfo("Command Result", "Terminal command executed successfully.")

def trigger_terminal_command_submit_data():
    """Function to trigger the submission of terminal command and clear the console."""
    clear_console()
    send_command_message()
    threading.Thread(target=execute_put_command).start()

def execute_put_command():
    """Function to execute a PUT command using the entered parameters."""
    try:
        # Retrieve values from the input fields
        ip_address = ip_entry.get()
        port = port_entry.get()
        frequency = freq_combobox.get()
        bandwidth = bw_combobox.get()
        ratio = ratio_combobox.get()
        power = power_combobox.get()

        # Construct the command to be executed
        command = (
            f"curl -X PUT https://{ip_address}:{port}/5g/bs/conf -k -u admin:admin -d "
            f"'{{\"Name\": \"BS-114\", \"ID\": \"14\", \"Band\": \"78\", \"Bandwidth\": \"{bandwidth}\", "
            f"\"Frequency\": \"{frequency}\", \"Ratio\": \"{ratio}\", \"Power\": \"{power}\", \"Sync\": \"free\"}}' "
            f"-H \"Content-Type: application/json\" -v"
        )

        # Run the command in a subprocess
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout

        # Update the output text widget with the result
        output_text.after(0, output_text.delete, "end-2l", "end-1l")
        output_text.after(0, output_text.insert, tk.END, output)

        # Check if the data was received successfully
        if "data received" in output.lower():
            output_text.after(0, output_text.delete, "1.0", tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Add a global variable to keep track of the keypad window
keypad_window = None

def open_keypad(entry_widget=None):
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
        if target == "Frequency":
            freq_combobox.delete(0, tk.END)
            freq_combobox.insert(tk.END, value)
        elif target == "Bandwidth":
            bw_combobox.delete(0, tk.END)
            bw_combobox.insert(tk.END, value)
        elif target == "Ratio":
            ratio_combobox.delete(0, tk.END)
            ratio_combobox.insert(tk.END, value)
        elif target == "Power":
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
