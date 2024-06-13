import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle
import subprocess
import threading
import json
from PIL import Image, ImageTk

wicon_logo_path = "/home/pi/Desktop/MECSware_Interface/logos/wicon_logo.png"
campus_6g_logo_path = "/home/pi/Desktop/MECSware_Interface/logos/6G_Campus.png"
wicon_6g_logo_path = "/home/pi/Desktop/MECSware_Interface/logos/wicon_6g_campus_logo.png"
logo_path = "/home/pi/Desktop/MECSware_Interface/logos/rptu_wicon_6g_campus_logo.png"

# Global variables to store the retrieved values
frequency_value = ""
bandwidth_value = ""
power_value = ""

# Create a list of options for each combobox
freq_options = ["3710", "3720", "3730", "3740", "3750", "3760", "3770", "3780", "3790"]
bw_options = ["20", "40", "50", "60", "80", "90", "100"]
ratio_options = ["5:5", "7:3", "4:1"]
power_options = ["0", "2", "4", "6", "8", "10", "12", "14", "16", "18", "20"]

# Initial setup values
ip_initial = "10.0.1.2"
port_initial = "6327"
name_initial = "BS-114"
id_initial = "14"
band_initial = "78"
freq_initial = "3710"
bw_initial = "20"
ratio_initial = "5:5"
power_initial = "10"

# Create a style for bold text
bold_font = ('TkDefaultFont', 20, 'bold')
Entries_bold_font = ('TkDefaultFont', 18, 'bold')
standard_font = ('TkDefaultFont', 18)
button_font = ('TkDefaultFont', 25)
mini_button_font = ('TkDefaultFont', 15)


# Create the main window
root = tk.Tk()
root.title("MECSware Interface")

# Setup for fullscreen, keyboard needed to close, or click on wicon logo
#root.attributes('-fullscreen', True)
# Press Escape to exit fullscreen
#root.bind("<Escape>", lambda event: root.attributes('-fullscreen', False))  

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

# Configure the background color for the frame and label styles
style.configure('TFrame', background='ghost white')
style.configure('TLabel', background='ghost white')

# Create style for buttons
style.configure('Standard.TButton', font=button_font)
style.configure('Mini.TButton', font=mini_button_font)

# Configure the main grid to be resizable
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create the main frame with padding
frame = ttk.Frame(root, padding="20", style='TFrame')
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
frame.config(style='TFrame')  # Set style to ensure consistency
for i in range(8):
    frame.columnconfigure(i, weight=1)

# Set minimum height for all rows to make them taller
for i in range(8):
    frame.grid_rowconfigure(i, minsize=90)  # Adjust the value as needed

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
            f"'{{\"Name\": \"BS-114\", \"ID\": \"{id_initial}\", \"Band\": \"78\", \"Bandwidth\": \"{bandwidth}\", "
            f"\"Frequency\": \"{frequency}\", \"Ratio\": \"{ratio}\", \"Power\": \"{power}\", \"Sync\": \"free\"}}' "
            f"-H \"Content-Type: application/json\" -v"
        )

        # Run the command in a subprocess with a timeout
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        #result = subprocess.run(command, shell=True, capture_output=True, text=True)
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
        #result = subprocess.run(command, shell=True, capture_output=True, text=True)
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
    combobox_entry = ttk.Entry(frame, justify='center', font=standard_font, width=8)
    combobox_entry.grid(row=row, column=column, padx=(100, 0), pady=10)

    # Create a Listbox to act as the dropdown list with a scrollbar
    listbox_frame = tk.Frame(frame)
    listbox = tk.Listbox(listbox_frame, font=('TkDefaultFont', 28), width=10, height=len(options))

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
    
    dropdown_button = ttk.Button(frame, text="▼", command=toggle_dropdown, width=5, style='Standard.TButton')
    dropdown_button.grid(row=row, column=column + 1, padx=(0, 0))

    listbox_frame.place_forget()

    return combobox_entry

# Function to resize the image
def resize_image(event):
    new_width = event.width // 2  # Adjust the scale as needed
    new_height = int(new_width * aspect_ratio)
    resized_image = original_image.resize((new_width, new_height), Image.ANTIALIAS)
    logo = ImageTk.PhotoImage(resized_image)
    logo_label.config(image=logo)
    logo_label.image = logo  # Keep a reference to avoid garbage collection

# Load and display the logo image
try:
    original_image = Image.open(logo_path)
    original_image = original_image.convert("RGBA")  # Ensure the image has an alpha channel for transparency
    aspect_ratio = original_image.height / original_image.width
    initial_width = 400
    initial_height = int(initial_width * aspect_ratio)
    resized_image = original_image.resize((initial_width, initial_height), Image.ANTIALIAS)
    logo = ImageTk.PhotoImage(resized_image)
    logo_label = tk.Label(frame, image=logo, bg="ghost white")
    logo_label.grid(row=0, column=5, rowspan=3, columnspan=4, pady=(50, 0))  # Adjust the position as needed
except Exception as e:
    messagebox.showerror("Error", f"Unable to load image: {e}")

width_c = 15

# Create labels and entry fields for Name, ID, and Band
name_label = ttk.Label(frame, text="Name:", width=width_c-5, anchor=tk.E, font = standard_font)
name_label.grid(row=4, column=5)
name_entry = ttk.Entry(frame, width=width_c-5, font = standard_font)
name_entry.insert(0, name_initial)
name_entry.grid(row=4, column=6, sticky=tk.W)

id_label = ttk.Label(frame, text="ID:", width=width_c-5, anchor=tk.E, font = standard_font)
id_label.grid(row=5, column=5)
id_entry = ttk.Entry(frame, width=width_c-10, font = standard_font)
id_entry.insert(0, id_initial)
id_entry.grid(row=5, column=6, sticky=tk.W)

band_label = ttk.Label(frame, text="Band:", width=width_c-5, anchor=tk.E, font = standard_font)
band_label.grid(row=5, column=7)
band_entry = ttk.Entry(frame, width=width_c-10, font = standard_font)
band_entry.insert(0, band_initial)
band_entry.grid(row=5, column=8, sticky=tk.W, padx=(0,100))

# Create labels and entry fields for IP Address and Port
ip_label = ttk.Label(frame, text="IP Address:", width=width_c, anchor=tk.E, font = standard_font)
ip_label.grid(row=0, column=0, columnspan=1)
ip_entry = ttk.Entry(frame, width=width_c, justify='center', font = standard_font)
ip_entry.insert(0, ip_initial)
ip_entry.grid(row=0, column=1, columnspan=1)

port_label = ttk.Label(frame, text="Port:", width=width_c, anchor=tk.E, font = standard_font)
port_label.grid(row=0, column=2)
port_entry = ttk.Entry(frame, width=width_c-5, justify='center', font = standard_font)
port_entry.insert(0, port_initial)
port_entry.grid(row=0, column=3, columnspan=1, padx=(10, 10))

# Create labels for current and desired settings
x_spacing = 50
y_spacing = 20

current_settings_label = ttk.Label(frame, text="Current Settings", width=width_c, anchor=tk.CENTER, font=bold_font)
current_settings_label.grid(row=1, column=1, columnspan=1, pady=y_spacing, padx=x_spacing)

desired_settings_label = ttk.Label(frame, text="Desired Settings", width=width_c, anchor=tk.CENTER, font=bold_font)
desired_settings_label.grid(row=1, column=2, columnspan=2, pady=y_spacing, padx=x_spacing)

freq_label = ttk.Label(frame, text="[MHz]", width=width_c-8, anchor=tk.W, font=Entries_bold_font)
freq_label.grid(row=2, column=4, pady=(5), padx=(0, 120), sticky=tk.W)

bw_label = ttk.Label(frame, text="[MHz]", width=width_c-8, anchor=tk.W, font=Entries_bold_font)
bw_label.grid(row=3, column=4, pady=(10,0), padx=(0, 120), sticky=tk.W)

ratio_label = ttk.Label(frame, text="Ratio:", width=width_c, anchor=tk.E, font=Entries_bold_font)
ratio_label.grid(row=4, column=0)

power_label = ttk.Label(frame, text="[dBm]", width=width_c-8, anchor=tk.W, font=Entries_bold_font)
power_label.grid(row=5, column=4, pady=(10,0), padx=(0, 120), sticky=tk.W)

# Create custom comboboxes for frequency, bandwidth, ratio, and power
freq_combobox = create_custom_combobox(row=2, column=2, options=freq_options, default_value=freq_initial)
bw_combobox = create_custom_combobox(row=3, column=2, options=bw_options, default_value=bw_initial)
ratio_combobox = create_custom_combobox(row=4, column=2, options=ratio_options, default_value=ratio_initial)
power_combobox = create_custom_combobox(row=5, column=2, options=power_options, default_value=power_initial)

# Create labels to display the current settings
current_freq_label = ttk.Label(frame, text="Frequency:", width=width_c, anchor=tk.E, font=Entries_bold_font)
current_freq_label.grid(row=2, column=0, pady=(5))
frequency_label = ttk.Label(frame, text="", width=width_c-10, anchor=tk.W, justify='center', font=standard_font)
frequency_label.grid(row=2, column=1, pady=(5))

current_bw_label = ttk.Label(frame, text="Bandwidth:", width=width_c, anchor=tk.E, font=Entries_bold_font)
current_bw_label.grid(row=3, column=0, pady=5)
bandwidth_label = ttk.Label(frame, text="", width=width_c-10, anchor=tk.W, justify='center', font=standard_font)
bandwidth_label.grid(row=3, column=1, pady=5)

current_power_label = ttk.Label(frame, text="Power:", width=width_c, anchor=tk.E, font=Entries_bold_font)
current_power_label.grid(row=5, column=0, pady=5)
power_label = ttk.Label(frame, text="", width=width_c-10, anchor=tk.W, justify='center', font=standard_font)
power_label.grid(row=5, column=1, pady=5)

# Create a button to test the connection
test_button = ttk.Button(frame, text="Test Connection", command=ping_command, style='Mini.TButton')
test_button.grid(row=0, column=4, pady=5, columnspan=2, sticky=tk.W, padx=(50, 20))

# Create a button to get current data
get_data_button = ttk.Button(frame, text="Get Data", command=get_current_data, style='Standard.TButton')
get_data_button.grid(row=6, column=1, pady=(15,5), columnspan=1)

# Create a button to submit the command
submit_button = ttk.Button(frame, text="Submit Data", command=submit_command, style='Standard.TButton')
submit_button.grid(row=6, column=2, pady=(15, 5), columnspan=2)

# Create a button to open input window
keypad_button = ttk.Button(frame, text="Keypad", width=width_c-6, command=lambda: open_keypad(None), style='Mini.TButton')
keypad_button.grid(row=6, column=8, pady=(15, 5), padx=(50, 50), columnspan=1, sticky=tk.W)

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
output_text = tk.Text(frame, bg="black", fg="white", font=('TkDefaultFont', 20))
output_text.grid(row=7, column=0, columnspan=9, pady=(15,0), padx=(30,20), sticky="nsew")

# Start the main event loop
root.mainloop()
