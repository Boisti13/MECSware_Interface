import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle
import subprocess
import threading
import json
from PIL import Image, ImageTk

# Constants
LOGO_PATH = "/home/pi/Desktop/MECSware_Interface/logos/wicon_logo.png"
TIMEOUT = 30
BOLD_FONT = ('TkDefaultFont', 12, 'bold')
ENTRIES_BOLD_FONT = ('TkDefaultFont', 10, 'bold')
WIDTH_C = 15

# Initial setup values
INITIAL_VALUES = {
    'ip': "10.0.1.2",
    'port': "6327",
    'name': "BS-114",
    'id': "14",
    'band': "78",
    'freq': "3700",
    'bw': "5",
    'ratio': "5:5",
    'power': "10"
}

# Options for comboboxes
OPTIONS = {
    'freq': ["3700", "3705", "3710", "3715"],
    'bw': ["5", "10", "15", "20"],
    'ratio': ["5:5", "7:3", "4:1"],
    'power': ["10", "12", "14", "16", "18", "20"]
}

# Global variables to store the retrieved values
frequency_value = ""
bandwidth_value = ""
power_value = ""

# Create the main window
root = tk.Tk()
root.title("MECSware Interface")

# Setup for max window size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

# Set the theme for the application
style = ThemedStyle(root)
style.set_theme("adapta")  # Replace "adapta" with your desired theme

# Configure the main grid to be resizable
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create the main frame with padding
frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
for i in range(8):
    frame.columnconfigure(i, weight=1)

# Functions

def clear_console():
    """Clears the console."""
    output_text.delete("1.0", tk.END)

def send_command_message():
    """Displays a message indicating the command is being sent."""
    output_text.insert(tk.END, "Sending command... Waiting for confirmation.\n")

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

        # Run the command in a subprocess with a timeout
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=TIMEOUT)
        output = result.stdout

        # Update the output text widget with the result
        output_text.after(0, output_text.delete, "end-2l", "end-1l")
        output_text.after(0, output_text.insert, tk.END, output)

        # Check if the data was received successfully
        if "data received" in output.lower():
            output_text.after(0, output_text.delete, "1.0", tk.END)
    except subprocess.TimeoutExpired:
        messagebox.showerror("Error", "No data received within 30 seconds. Operation timed out.")
        clear_console()  # Clear the internal terminal window
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        clear_console()  # Clear the internal terminal window

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

def submit_command():
    """Function to submit a command and show a confirmation message."""
    trigger_terminal_command_submit_data()
    messagebox.showinfo("Command Result", "Terminal command executed successfully.")

def ping_command():
    """Function to start the ping test in a separate thread."""
    threading.Thread(target=ping_test).start()

def show_waiting_message():
    """Function to display a waiting message in the console."""
    clear_console()
    output_text.insert(tk.END, "Waiting for response from server...\n")
    output_text.see(tk.END)
    output_text.update_idletasks()

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
        # Run the command in a subprocess with a timeout
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=TIMEOUT)
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
    except subprocess.TimeoutExpired:
        messagebox.showerror("Error", "No data received within 30 seconds. Operation timed out.")
        clear_console()  # Clear the internal terminal window
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        clear_console()  # Clear the internal terminal window

def execute_command():
    """Function to execute an arbitrary command."""
    try:
        # Retrieve the command from the input field
        command = command_entry.get()
        # Run the command in a subprocess
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output_text.insert(tk.END, result.stdout)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to handle closing any open list
def close_open_lists(event):
    for child in frame.winfo_children():
        if isinstance(child, tk.Frame):
            child.place_forget()

# Bind the function to close open lists to the left mouse click event on the root window
root.bind("<Button-1>", close_open_lists)

# Create a function to set up a custom combobox
def create_custom_combobox(row, column, options, default_value):
    # Create a combobox-like entry widget
    combobox_entry = ttk.Entry(frame, justify='right')
    combobox_entry.grid(row=row, column=column, padx=10, pady=10)

    # Create a Listbox to act as the dropdown list with a scrollbar
    listbox_frame = tk.Frame(frame)
    listbox = tk.Listbox(listbox_frame, font=('TkDefaultFont', 20), width=20)
    scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=listbox.yview)
    listbox.config(yscrollcommand=scrollbar.set)

    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Populate the listbox with options
    for option in options:
        # Center-align text by adding spaces
        listbox.insert(tk.END, f'{option:^20}')

    def select_item(event):
        """Function to handle item selection"""
        selection = listbox.curselection()
        if selection:
            selected_item = listbox.get(selection).strip()
            combobox_entry.delete(0, tk.END)
            combobox_entry.insert(0, selected_item)
            listbox_frame.place_forget()

    # Bind the selection event to the Listbox
    listbox.bind("<<ListboxSelect>>", select_item)

    def toggle_dropdown(event=None):
        """Function to show/hide the dropdown list"""
        close_open_lists(None)
        if not listbox_frame.winfo_ismapped():
            listbox_frame.place(x=combobox_entry.winfo_x(), y=combobox_entry.winfo_y() + combobox_entry.winfo_height())
            listbox_frame.lift()

    def filter_options(event):
        """Function to filter options based on entry text"""
        typed = combobox_entry.get()
        listbox.delete(0, tk.END)
        for option in options:
            if typed.lower() in option.lower():
                # Center-align text by adding spaces
                listbox.insert(tk.END, f'{option:^20}')
        if listbox.size() > 0:
            toggle_dropdown()

    combobox_entry.bind("<KeyRelease>", filter_options)
    combobox_entry.bind("<Button-1>", lambda event: open_keypad(combobox_entry))
    combobox_entry.insert(0, default_value)
    
    dropdown_button = ttk.Button(frame, text="▼", command=toggle_dropdown)
    dropdown_button.grid(row=row, column=column + 1, padx=(0, 10))

    listbox_frame.place_forget()

    return combobox_entry

# Load and display the logo image
try:
    image = Image.open(LOGO_PATH)
    image = image.convert("RGBA")  # Ensure the image has an alpha channel for transparency
    image_resized = image.resize((180, 70), Image.ANTIALIAS)
    logo = ImageTk.PhotoImage(image_resized)
    logo_label = tk.Label(frame, image=logo, bg="ghost white")
    logo_label.grid(row=0, column=6, rowspan=2, columnspan=2)  # Adjust the position as needed
except Exception as e:
    messagebox.showerror("Error", f"Unable to load image: {e}")

# Create labels and entry fields for Name, ID, and Band
def create_label_entry(row, column, text, initial_value, width=WIDTH_C-5):
    label = ttk.Label(frame, text=text, width=width, anchor=tk.E)
    label.grid(row=row, column=column)
    entry = ttk.Entry(frame, width=width)
    entry.insert(0, initial_value)
    entry.grid(row=row, column=column+1, sticky=tk.W)
    return entry

name_entry = create_label_entry(3, 6, "Name:", INITIAL_VALUES['name'])
id_entry = create_label_entry(4, 6, "ID:", INITIAL_VALUES['id'])
band_entry = create_label_entry(5, 6, "Band:", INITIAL_VALUES['band'])

ip_label = ttk.Label(frame, text="IP Address:", width=WIDTH_C, anchor=tk.E)
ip_label.grid(row=0, column=0, columnspan=1)
ip_entry = ttk.Entry(frame, width=WIDTH_C, justify='center')
ip_entry.insert(0, INITIAL_VALUES['ip'])
ip_entry.grid(row=0, column=1, columnspan=1)

port_label = ttk.Label(frame, text="Port:", width=WIDTH_C, anchor=tk.E)
port_label.grid(row=0, column=2)
port_entry = ttk.Entry(frame, width=WIDTH_C, justify='center')
port_entry.insert(0, INITIAL_VALUES['port'])
port_entry.grid(row=0, column=3, columnspan=1)

# Create labels for current and desired settings
x_spacing = 10
y_spacing = 20

current_settings_label = ttk.Label(frame, text="Current Settings", width=WIDTH_C, anchor=tk.CENTER, font=BOLD_FONT)
current_settings_label.grid(row=1, column=1, columnspan=2, pady=y_spacing, padx=x_spacing)

desired_settings_label = ttk.Label(frame, text="Desired Settings", width=WIDTH_C, anchor=tk.CENTER, font=BOLD_FONT)
desired_settings_label.grid(row=1, column=3, columnspan=2, pady=y_spacing, padx=x_spacing)

freq_label = ttk.Label(frame, text="[MHz]", width=WIDTH_C-10, anchor=tk.W, font=ENTRIES_BOLD_FONT)
freq_label.grid(row=2, column=5, pady=(5), sticky=tk.W)

bw_label = ttk.Label(frame, text="[MHz]", width=WIDTH_C-10, anchor=tk.W, font=ENTRIES_BOLD_FONT)
bw_label.grid(row=3, column=5, pady=(10, 0), sticky=tk.W)

ratio_label = ttk.Label(frame, text="Ratio:", width=WIDTH_C, anchor=tk.E, font=ENTRIES_BOLD_FONT)
ratio_label.grid(row=4, column=0)

power_label = ttk.Label(frame, text="[dBm]", width=WIDTH_C-10, anchor=tk.W, font=ENTRIES_BOLD_FONT)
power_label.grid(row=5, column=5, pady=(10, 0), sticky=tk.W)

# Create custom comboboxes for frequency, bandwidth, ratio, and power
freq_combobox = create_custom_combobox(2, 3, OPTIONS['freq'], INITIAL_VALUES['freq'])
bw_combobox = create_custom_combobox(3, 3, OPTIONS['bw'], INITIAL_VALUES['bw'])
ratio_combobox = create_custom_combobox(4, 3, OPTIONS['ratio'], INITIAL_VALUES['ratio'])
power_combobox = create_custom_combobox(5, 3, OPTIONS['power'], INITIAL_VALUES['power'])

# Create labels to display the current settings
def create_current_label(row, column, text):
    label = ttk.Label(frame, text=text, width=WIDTH_C, anchor=tk.E, font=ENTRIES_BOLD_FONT)
    label.grid(row=row, column=column, pady=(5))
    value_label = ttk.Label(frame, text="", width=WIDTH_C, anchor=tk.W, justify='center')
    value_label.grid(row=row, column=column+1, pady=(5))
    return value_label

frequency_label = create_current_label(2, 0, "Frequency:")
bandwidth_label = create_current_label(3, 0, "Bandwidth:")
power_label = create_current_label(5, 0, "Power:")

# Create a button to test the connection
test_button = ttk.Button(frame, text="Test Connection", command=ping_command)
test_button.grid(row=0, column=4, pady=5, columnspan=2, sticky=tk.W)

# Create a button to get current data
get_data_button = ttk.Button(frame, text="Get Current Data", command=get_current_data)
get_data_button.grid(row=6, column=1, pady=(25, 15), columnspan=2)

# Create a button to submit the command
submit_button = ttk.Button(frame, text="Submit Command", command=submit_command)
submit_button.grid(row=6, column=3, pady=(25, 15), columnspan=2)

# Create a button to open input window
keypad_button = ttk.Button(frame, text="Keypad", width=WIDTH_C-5, command=lambda: open_keypad(None))
keypad_button.grid(row=6, column=7, pady=(0, 0), columnspan=1, sticky=tk.W)

# Bind the click event to close the window
logo_label.bind("<Button-1>", lambda event: root.destroy())

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

# Configure row and column weights to allow resizing
frame.grid_rowconfigure(7, weight=1)  # Row containing the output_text widget
frame.grid_columnconfigure(0, weight=1)

# Create a text widget to display the output
output_text = tk.Text(frame, bg="black", fg="white")
output_text.grid(row=7, column=0, columnspan=8, pady=(15, 0), padx=(30, 20), sticky="nsew")

# Start the main event loop
root.mainloop()
