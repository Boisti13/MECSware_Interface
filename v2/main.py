# main.py

import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle
import subprocess
import threading
import json
from PIL import Image, ImageTk
from keypad import open_keypad  # Import the open_keypad function

logo_path = "/home/pi/Desktop/MECSware_Interface/logos/wicon_logo.png"

# Global variables to store the retrieved values
frequency_value = ""
bandwidth_value = ""
power_value = ""

# Create a list of options for each combobox
freq_options = ["3700", "3705", "3710", "3715"]
bw_options = ["5", "10", "15", "20"]
ratio_options = ["5:5", "7:3", "4:1"]
power_options = ["10", "12", "14", "16", "18", "20"]

# Initial setup values
ip_initial = "10.0.1.2"
port_initial = "6327"
name_initial = "BS-114"
id_initial = "14"
band_initial = "78"
freq_initial = "3700"
bw_initial = "5"
ratio_initial = "5:5"
power_initial = "10"

# Create a style for bold text
bold_font = ('TkDefaultFont', 12, 'bold')
Entries_bold_font = ('TkDefaultFont', 10, 'bold')

# Create the main window
root = tk.Tk()
root.title("MECSware Interface")
# Setup for fullscreen, keyboard needed to close
##root.attributes('-fullscreen', True)
##root.bind("<Escape>", lambda event: root.attributes('-fullscreen', False))  # Press Escape to exit fullscreen

# Setup for max window size
# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
    
# Set the window size to the screen size
root.geometry(f"{screen_width}x{screen_height}")

# Setup for specific window size at start
#root.geometry("800x600")  # Initial size of the window

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
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
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
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
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
    combobox_entry.bind("<Button-1>", lambda event: open_keypad(root, freq_combobox, bw_combobox, ratio_combobox, power_combobox))
    combobox_entry.insert(0, default_value)
    
    dropdown_button = ttk.Button(frame, text="▼", command=toggle_dropdown)
    dropdown_button.grid(row=row, column=column + 1, padx=(0, 10))

    listbox_frame.place_forget()

    return combobox_entry

# Load and display the logo image
try:
    image = Image.open(logo_path)
    image = image.convert("RGBA")  # Ensure the image has an alpha channel for transparency
    image_resized = image.resize((180, 70), Image.ANTIALIAS)
    logo = ImageTk.PhotoImage(image_resized)
    logo_label = tk.Label(frame, image=logo, bg="ghost white")
    logo_label.grid(row=0, column=6, rowspan=2, columnspan=2)  # Adjust the position as needed
except Exception as e:
    messagebox.showerror("Error", f"Unable to load image: {e}")

width_c = 15

# Create labels and entry fields for Name, ID, and Band
name_label = ttk.Label(frame, text="Name:", width=width_c-5, anchor=tk.E)
name_label.grid(row=3, column=6)
name_entry = ttk.Entry(frame, width=width_c-5)
name_entry.insert(0, name_initial)
name_entry.grid(row=3, column=7, sticky=tk.W)

id_label = ttk.Label(frame, text="ID:", width=width_c-5, anchor=tk.E)
id_label.grid(row=4, column=6)
id_entry = ttk.Entry(frame, width=width_c-5)
id_entry.insert(0, id_initial)
id_entry.grid(row=4, column=7, sticky=tk.W)

band_label = ttk.Label(frame, text="Band:", width=width_c-5, anchor=tk.E)
band_label.grid(row=5, column=6)
band_entry = ttk.Entry(frame, width=width_c-5)
band_entry.insert(0, band_initial)
band_entry.grid(row=5, column=7, sticky=tk.W)

# Create labels and entry fields for IP Address and Port
ip_label = ttk.Label(frame, text="IP Address:", width=width_c, anchor=tk.E)
ip_label.grid(row=0, column=0, columnspan=1)
ip_entry = ttk.Entry(frame, width=width_c, justify='center')
ip_entry.insert(0, ip_initial)
ip_entry.grid(row=0, column=1, columnspan=1)

port_label = ttk.Label(frame, text="Port:", width=width_c, anchor=tk.E)
port_label.grid(row=0, column=2)
port_entry = ttk.Entry(frame, width=width_c, justify='center')
port_entry.insert(0, port_initial)
port_entry.grid(row=0, column=3, columnspan=1)

# Create labels for current and desired settings
x_spacing = 10
y_spacing = 20

current_settings_label = ttk.Label(frame, text="Current Settings", width=width_c, anchor=tk.CENTER, font=bold_font)
current_settings_label.grid(row=1, column=1, columnspan=2, pady=y_spacing, padx=x_spacing)

desired_settings_label = ttk.Label(frame, text="Desired Settings", width=width_c, anchor=tk.CENTER, font=bold_font)
desired_settings_label.grid(row=1, column=3, columnspan=2, pady=y_spacing, padx=x_spacing)

freq_label = ttk.Label(frame, text="[MHz]", width=width_c-10, anchor=tk.W, font=Entries_bold_font)
freq_label.grid(row=2, column=5, pady=(5), sticky=tk.W)

bw_label = ttk.Label(frame, text="[MHz]", width=width_c-10, anchor=tk.W, font=Entries_bold_font)
bw_label.grid(row=3, column=5, pady=(10,0), sticky=tk.W)

ratio_label = ttk.Label(frame, text="Ratio:", width=width_c, anchor=tk.E, font=Entries_bold_font)
ratio_label.grid(row=4, column=0)

power_label = ttk.Label(frame, text="[dBm]", width=width_c-10, anchor=tk.W, font=Entries_bold_font)
power_label.grid(row=5, column=5, pady=(10,0), sticky=tk.W)

# Create custom comboboxes for frequency, bandwidth, ratio, and power
freq_combobox = create_custom_combobox(row=2, column=3, options=freq_options, default_value=freq_initial)
bw_combobox = create_custom_combobox(row=3, column=3, options=bw_options, default_value=bw_initial)
ratio_combobox = create_custom_combobox(row=4, column=3, options=ratio_options, default_value=ratio_initial)
power_combobox = create_custom_combobox(row=5, column=3, options=power_options, default_value=power_initial)

# Create labels to display the current settings
current_freq_label = ttk.Label(frame, text="Frequency:", width=width_c, anchor=tk.E, font=Entries_bold_font)
current_freq_label.grid(row=2, column=0, pady=(5))
frequency_label = ttk.Label(frame, text="", width=width_c, anchor=tk.W, justify='center')
frequency_label.grid(row=2, column=1, pady=(5))

current_bw_label = ttk.Label(frame, text="Bandwidth:", width=width_c, anchor=tk.E, font=Entries_bold_font)
current_bw_label.grid(row=3, column=0, pady=5)
bandwidth_label = ttk.Label(frame, text="", width=width_c, anchor=tk.W, justify='center')
bandwidth_label.grid(row=3, column=1, pady=5)

current_power_label = ttk.Label(frame, text="Power:", width=width_c, anchor=tk.E, font=Entries_bold_font)
current_power_label.grid(row=5, column=0, pady=5)
power_label = ttk.Label(frame, text="", width=width_c, anchor=tk.W, justify='center')
power_label.grid(row=5, column=1, pady=5)

# Create a button to test the connection
test_button = ttk.Button(frame, text="Test Connection", command=ping_command)
test_button.grid(row=0, column=4, pady=5, columnspan=2, sticky=tk.W)

# Create a button to get current data
get_data_button = ttk.Button(frame, text="Get Current Data", command=get_current_data)
get_data_button.grid(row=6, column=1, pady=(25,15), columnspan=2)

# Create a button to submit the command
submit_button = ttk.Button(frame, text="Submit Command", command=submit_command)
submit_button.grid(row=6, column=3, pady=(25, 15), columnspan=2)

# Create a button to open input window
keypad_button = ttk.Button(frame, text="Keypad", width=width_c-5, command=lambda: open_keypad(root, freq_combobox, bw_combobox, ratio_combobox, power_combobox))
keypad_button.grid(row=6, column=7, pady=(0, 0), columnspan=1, sticky=tk.W)

# Bind the click event to close the window
logo_label.bind("<Button-1>", lambda event: root.destroy())

# Configure row and column weights to allow resizing
frame.grid_rowconfigure(7, weight=1)  # Row containing the output_text widget
frame.grid_columnconfigure(0, weight=1)

# Create a text widget to display the output
output_text = tk.Text(frame, bg="black", fg="white")
output_text.grid(row=7, column=0, columnspan=8, pady=(15,0), padx=(30,20), sticky="nsew")

# Start the main event loop
root.mainloop()
