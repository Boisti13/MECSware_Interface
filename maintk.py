import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
import subprocess
import threading
from ttkthemes import ThemedStyle


# Global variables to store the retrieved values
frequency_value = ""
bandwidth_value = ""
ratio_value = ""
power_value = ""

def trigger_terminal_command():
    ip_address = ip_entry.get()
    port = port_entry.get()
    frequency = freq_combobox.get()
    bandwidth = bw_combobox.get()
    ratio = ratio_combobox.get()
    power = power_combobox.get()

    command = f"curl -X PUT https://{ip_address}:{port}/5g/bs/conf -k -u admin:admin -d '{{\"Name\": \"BS-114\", \"ID\": \"14\", \"Band\": \"78\", \"Bandwidth\": \"{bandwidth}\", \"Frequency\": \"{frequency}\", \"Ratio\": \"{ratio}\", \"Power\": \"{power}\", \"Sync\": \"free\"}}' -H \"Content-Type: application/json\" -v"

    subprocess.run(command, shell=True)

def ping_test():
    ip_address = ip_entry.get()
    try:
        subprocess.run(['ping', '-c', '1', ip_address], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        messagebox.showinfo("Ping Result", "Ping successful!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Ping Result", "Ping failed!")

def submit_command():
    trigger_terminal_command()
    messagebox.showinfo("Command Result", "Terminal command executed successfully.")

def ping_command():
    threading.Thread(target=ping_test).start()

def get_current_data():
    global frequency_value, bandwidth_value, ratio_value, power_value

    ip_address = ip_entry.get()
    port = port_entry.get()
    name = name_entry.get()

    command = f"curl -X GET https://{ip_address}:{port}/5g/bs/status/{name} -k -u admin:admin"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout

    try:
        data = json.loads(output)
        frequency_value = data.get("frequency", "")
        bandwidth_value = data.get("bandwidth", "")
        ratio_value = data.get("ratio", "")
        power_value = data.get("power", "")

        messagebox.showinfo("Current Data", f"Frequency: {frequency_value}\nBandwidth: {bandwidth_value}\nRatio: {ratio_value}\nPower: {power_value}")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Failed to retrieve current data.")

root = tk.Tk()
root.title("Dropdown Test")

style = ThemedStyle(root)
style.set_theme("breeze")  # Replace "arc" with your desired theme

frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

########################################################################

logo = tk.PhotoImage(file="/home/pi/Desktop/logo.png")
# Resize the logo to 50x100 pixels
logo_resized = logo.subsample(logo.width() // 140, logo.height() // 70)

# Create a label to display the resized logo image
#logo_label = tk.Label(root, image=logo_resized)
#logo_label.place(x=260, y=250)  # Position the logo at (0, 0)

########################################################################

# Create a custom style for the dropdown menu
dropdown_style = ttk.Style()
dropdown_style.configure("Custom.TCombobox", background="light blue")  # Change "light blue" to your desired background color

# Create labels and entry fields for Name, ID, and Band

band_label = ttk.Label(frame, text="")
band_label.grid(row=1, column=2, sticky=tk.E)

name_label = ttk.Label(frame, text="Name:")
name_label.grid(row=2, column=3, sticky=tk.E)
name_entry = ttk.Entry(frame, width=6)
name_entry.insert(0, "BS-114")
name_entry.grid(row=2, column=4, pady=(0, 5))

id_label = ttk.Label(frame, text="ID:")
id_label.grid(row=3, column=3, sticky=tk.E)
id_entry = ttk.Entry(frame, width=6)
id_entry.insert(0, "14")
id_entry.grid(row=3, column=4, pady=(0, 5))

band_label = ttk.Label(frame, text="Band:")
band_label.grid(row=4, column=3, sticky=tk.E)
band_entry = ttk.Entry(frame, width=6)
band_entry.insert(0, "78")
band_entry.grid(row=4, column=4, pady=(0, 5))

ip_label = ttk.Label(frame, text="IP Address:")
ip_label.grid(row=0, column=0, sticky=tk.E)
ip_entry = ttk.Entry(frame, width=15)
ip_entry.insert(0, "10.0.1.2")
ip_entry.grid(row=0, column=1, pady=(0, 5))

port_label = ttk.Label(frame, text="Port:")
port_label.grid(row=0, column=2, sticky=tk.E)
port_entry = ttk.Entry(frame, width=6)
port_entry.insert(0, "6327")
port_entry.grid(row=0, column=3, pady=(0, 5))

############

bw_label = ttk.Label(frame, text="Bandwidth:")
bw_label.grid(row=2, column=0, sticky=tk.E)
bw_combobox = ttk.Combobox(frame, values=["100", "90", "80", "60", "50", "40", "20"], width=8)
bw_combobox.grid(row=2, column=1, pady=(0, 5))
bw_combobox.set("60")
bw_unit_label = ttk.Label(frame, text="Hz")
bw_unit_label.grid(row=2, column=2, sticky=tk.W)

freq_label = ttk.Label(frame, text="Frequency:")
freq_label.grid(row=3, column=0, sticky=tk.E)
freq_combobox = ttk.Combobox(frame, values=["3770", "3750", "3720", "3770"], width=8)
freq_combobox.grid(row=3, column=1, pady=(0, 5))
freq_combobox.set("3770")
freq_unit_label = ttk.Label(frame, text="Hz")
freq_unit_label.grid(row=3, column=2, sticky=tk.W)

ratio_label = ttk.Label(frame, text="Ratio:")
ratio_label.grid(row=4, column=0, sticky=tk.E)
ratio_combobox = ttk.Combobox(frame, values=["5:5", "7:3", "4:1"], width=8)
ratio_combobox.grid(row=4, column=1, pady=(0, 5))
ratio_combobox.set("5:5")

power_label = ttk.Label(frame, text="Power:")
power_label.grid(row=5, column=0, sticky=tk.E)
power_combobox = ttk.Combobox(frame, values=["20", "20", "20"], width=8)
power_combobox.grid(row=5, column=1, pady=(0, 5))
power_combobox.set("20")
power_unit_label = ttk.Label(frame, text="dBm")
power_unit_label.grid(row=5, column=2, sticky=tk.W)

ping_button = ttk.Button(frame, text="Ping", command=ping_command, width=8, style="classic.TButton")
ping_button.grid(row=0, column=4, rowspan=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 5))

submit_button = ttk.Button(frame, text="Submit", command=submit_command, width=10)
submit_button.grid(row=6, column=0, columnspan=1, pady=(20, 0), padx=(50, 0), sticky=(tk.W, tk.E))

get_current_data_button = ttk.Button(frame, text="Get Data", command=get_current_data, width=10)
get_current_data_button.grid(row=6, column=2, columnspan=1, pady=(20, 0), padx=(50, 0), sticky=(tk.W, tk.E))

exit_button = ttk.Button(frame, text="Exit", command=root.destroy, width=8)
exit_button.grid(row=8, column=4, columnspan=1, pady=(20, 0), padx=(0, 50), sticky=(tk.W, tk.E, tk.N, tk.S))

###################################
# Labels to display the retrieved data
frequency_label = ttk.Label(frame, text="")
frequency_label.grid(row=7, column=0, columnspan=2, pady=(20, 0), padx=(50, 0), sticky=(tk.W, tk.E))

bandwidth_label = ttk.Label(frame, text="")
bandwidth_label.grid(row=7, column=2, columnspan=2, pady=(20, 0), padx=(50, 0), sticky=(tk.W, tk.E))

ratio_label = ttk.Label(frame, text="")
ratio_label.grid(row=8, column=0, columnspan=2, pady=(20, 0), padx=(50, 0), sticky=(tk.W, tk.E))

power_label = ttk.Label(frame, text="")
power_label.grid(row=8, column=2, columnspan=2, pady=(20, 0), padx=(50, 0), sticky=(tk.W, tk.E))
#################################

root.mainloop()
