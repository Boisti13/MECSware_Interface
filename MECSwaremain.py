# Import necessary libraries
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedStyle
import subprocess
import threading
import json
from PIL import Image, ImageTk

# Global variables to store the retrieved values
frequency_value = ""
bandwidth_value = ""
power_value = ""

def trigger_terminal_command_submit_data():
    """Function to trigger the submission of terminal command and clear the console."""
    # Clear console
    output_text.delete("1.0", tk.END)
    # Print a message in the internal console before sending the PUT command
    output_text.insert(tk.END, "Sending command... Waiting for confirmation.\n")
    # Run the PUT command in a separate thread
    threading.Thread(target=execute_put_command).start()

def execute_put_command():
    """Function to execute a PUT command using the entered parameters."""
    ip_address = ip_entry.get()
    port = port_entry.get()
    frequency = freq_combobox.get()
    bandwidth = bw_combobox.get()
    ratio = ratio_combobox.get()
    power = power_combobox.get()

    command = (f"curl -X PUT https://{ip_address}:{port}/5g/bs/conf -k -u admin:admin -d "
               f"'{{\"Name\": \"BS-114\", \"ID\": \"14\", \"Band\": \"78\", \"Bandwidth\": \"{bandwidth}\", "
               f"\"Frequency\": \"{frequency}\", \"Ratio\": \"{ratio}\", \"Power\": \"{power}\", \"Sync\": \"free\"}}' "
               f"-H \"Content-Type: application/json\" -v")

    # Execute the command and capture the output
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout

    # Clear the waiting message
    output_text.delete("end-2l", "end-1l")

    # Display the output in the text widget
    output_text.insert(tk.END, output)

    # Check if data is received and remove the message from the internal console
    if "data received" in output.lower():
        output_text.delete("1.0", tk.END)

def ping_test():
    """Function to execute a ping test to the provided IP address."""
    global output_text

    ip_address = ip_entry.get()
    try:
        # Clear the contents of the text widget
        output_text.delete("1.0", tk.END)

        # Execute the ping command and capture the output
        result = subprocess.run(['ping', '-c', '1', ip_address], capture_output=True, text=True)
        output = result.stdout

        # Display the output in the text widget
        output_text.insert(tk.END, output)

        # Check if ping was successful and show a message box
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
    # Clear console
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "Waiting for response from server...\n")
    # Ensure the waiting message is visible by scrolling to the end of the text widget
    output_text.see(tk.END)
    # Update the GUI to ensure the waiting message is displayed immediately
    output_text.update_idletasks()

def get_current_data():
    """Function to get the current data from the server."""
    global frequency_value, bandwidth_value, power_value

    ip_address = ip_entry.get()
    port = port_entry.get()
    name = name_entry.get()

    command = (f"curl -X GET https://{ip_address}:{port}/5g/bs/status/{name} -k -u admin:admin "
               f"-H \"Content-Type: application/json\" -v")
    
    # Show waiting message
    show_waiting_message()

    # Execute the command and capture the output
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout

    # Clear the waiting message
    output_text.delete("end-2l", "end-1l")

    # Display the output in the text widget
    output_text.insert(tk.END, output)

    try:
        data = json.loads(output)
        frequency_value = data.get("frequency", "")
        bandwidth_value = data.get("bandwidth", "")
        power_value = data.get("tx_power", "")

        # Update the labels with the retrieved data
        frequency_label.config(text=f"{frequency_value}")
        bandwidth_label.config(text=f"{bandwidth_value}")
        power_label.config(text=f"{power_value}")

        messagebox.showinfo("Current Data", f"Frequency: {frequency_value}\nBandwidth: {bandwidth_value}\nPower: {power_value}")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Failed to retrieve current data.")

def execute_command():
    """Function to execute an arbitrary command."""
    command = command_entry.get()
    # Execute the command using subprocess and capture the output
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout

    # Display the output in the text widget
    output_text.insert(tk.END, output)

# Create a style for bold text
bold_font = ('TkDefaultFont', 12, 'bold')

# Create the main window
root = tk.Tk()
#root.title("Königlicher MECSware Manipulator")
root.title("MECSware Interface")

# Set the theme for the application
style = ThemedStyle(root)
style.set_theme("adapta")  # Replace "adapta" with your desired theme

# Create the main frame with padding
frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Load and display the logo image
image = Image.open("/home/pi/Desktop/MECSware_GUI/logo.png")
image = image.convert("RGBA")  # Ensure the image has an alpha channel for transparency
image_resized = image.resize((180, 70), Image.ANTIALIAS)
logo = ImageTk.PhotoImage(image_resized)
logo_label = tk.Label(root, image=logo, bg="ghost white")
logo_label.place(x=600, y=300)  # Adjust the position as needed

width_c = 15

# Create labels and entry fields for Name, ID, and Band
name_label = ttk.Label(frame, text="Name:", width=width_c-5, anchor=tk.E)
name_label.grid(row=3, column=4)
name_entry = ttk.Entry(frame, width=width_c-5)
name_entry.insert(0, "BS-114")
name_entry.grid(row=3, column=5)

id_label = ttk.Label(frame, text="ID:", width=width_c-5, anchor=tk.E)
id_label.grid(row=4, column=4)
id_entry = ttk.Entry(frame, width=width_c-5)
id_entry.insert(0, "14")
id_entry.grid(row=4, column=5)

band_label = ttk.Label(frame, text="Band:", width=width_c-5, anchor=tk.E)
band_label.grid(row=5, column=4)
band_entry = ttk.Entry(frame, width=width_c-5)
band_entry.insert(0, "78")
band_entry.grid(row=5, column=5)

# Create labels and entry fields for IP Address and Port
ip_label = ttk.Label(frame, text="IP Address:", width=width_c, anchor=tk.E)
ip_label.grid(row=0, column=0, columnspan=1)
ip_entry = ttk.Entry(frame, width=width_c, justify='center')
ip_entry.insert(0, "10.0.1.2")
ip_entry.grid(row=0, column=1, columnspan=1)

port_label = ttk.Label(frame, text="Port:", width=width_c, anchor=tk.E)
port_label.grid(row=0, column=2)
port_entry = ttk.Entry(frame, width=width_c, justify='center')
port_entry.insert(0, "6327")
port_entry.grid(row=0, column=3, columnspan=1)

# Create labels for current and desired settings
current_settings_label = ttk.Label(frame, text="Current Settings", width=width_c, anchor=tk.CENTER, font=bold_font)
current_settings_label.grid(row=2, column=1, pady=10)

desired_settings_label = ttk.Label(frame, text="Desired Settings", width=width_c, anchor=tk.CENTER, font=bold_font)
desired_settings_label.grid(row=2, column=2, pady=10)

# Create labels and comboboxes for Bandwidth, Frequency, Ratio, and Power
bw_label = ttk.Label(frame, text="Bandwidth:", width=width_c, anchor=tk.E)
bw_label.grid(row=3, column=0)

bw_combobox = ttk.Combobox(frame, values=["100", "90", "80", "60", "50", "40", "20"], width=width_c, justify='center')
bw_combobox.grid(row=3, column=2, pady=(10, 10))
bw_combobox.set("60")

freq_combobox = ttk.Combobox(frame, values=["3770", "3750", "3720", "3770"], width=width_c, justify='center')
freq_combobox.grid(row=4, column=2, pady=(10, 10))
freq_combobox.set("3730")

ratio_combobox = ttk.Combobox(frame, values=["5:5", "7:3", "4:1"], width=width_c, justify='center')
ratio_combobox.grid(row=5, column=2, pady=(10, 10))
ratio_combobox.set("5:5")

power_combobox = ttk.Combobox(frame, values=["20", "20", "20"], width=width_c, justify='center')
power_combobox.grid(row=6, column=2, pady=(10, 10))
power_combobox.set("20")

bw_unit_label = ttk.Label(frame, text="MHz", width=width_c-5)
bw_unit_label.grid(row=3, column=3)

freq_label = ttk.Label(frame, text="Frequency:", width=width_c, anchor=tk.E)
freq_label.grid(row=4, column=0)

freq_unit_label = ttk.Label(frame, text="MHz", width=width_c-5)
freq_unit_label.grid(row=4, column=3)

ratio_label = ttk.Label(frame, text="Ratio:", width=width_c, anchor=tk.E)
ratio_label.grid(row=5, column=0)

power_label = ttk.Label(frame, text="Power:", width=width_c, anchor=tk.E)
power_label.grid(row=6, column=0)

power_unit_label = ttk.Label(frame, text="dBm", width=width_c-5)
power_unit_label.grid(row=6, column=3)

# Create buttons for Ping, Submit, Get Data, and Exit
ping_button = ttk.Button(frame, text="Ping", command=ping_command, width=width_c-5, style="classic.Warning.TButton")
ping_button.grid(row=0, column=4, padx=15, pady=0)

submit_button = ttk.Button(frame, text="Submit", command=submit_command, width=width_c)
submit_button.grid(row=7, column=2, padx=10, pady=5)

get_current_data_button = ttk.Button(frame, text="Get Data", command=get_current_data, width=width_c)
get_current_data_button.grid(row=7, column=1, padx=10, pady=5)

exit_button = ttk.Button(frame, text="Exit", command=root.destroy, width=width_c)
exit_button.grid(row=10, column=4, columnspan=2, sticky=tk.E)

# Labels to display the retrieved data
frequency_label = ttk.Label(frame, text="", width=width_c, anchor=tk.E)
frequency_label.grid(row=4, column=1, columnspan=1)

bandwidth_label = ttk.Label(frame, text="", width=width_c, anchor=tk.E)
bandwidth_label.grid(row=3, column=1, columnspan=1)

power_label = ttk.Label(frame, text="", width=width_c, anchor=tk.E)
power_label.grid(row=6, column=1, columnspan=1)

# Create a text widget to display terminal output
output_text = tk.Text(frame, wrap="word", height=10, width=45, bg="black", fg="white")
output_text.grid(row=8, column=0, columnspan=6, padx=0, pady=20, sticky="nsew")

# Start the main event loop
root.mainloop()
