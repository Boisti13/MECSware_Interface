import tkinter as tk
from tkinter import ttk
from event_handlers import open_keypad, ping_command, get_current_data, submit_command
from utilities import create_custom_combobox

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

# Create a list of options for each combobox
freq_options = ["3700", "3705", "3710", "3715"]
bw_options = ["5", "10", "15", "20"]
ratio_options = ["5:5", "7:3", "4:1"]
power_options = ["10", "12", "14", "16", "18", "20"]

def setup_ui(frame):
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
    freq_combobox = create_custom_combobox(frame, row=2, column=3, options=freq_options, default_value=freq_initial)
    bw_combobox = create_custom_combobox(frame, row=3, column=3, options=bw_options, default_value=bw_initial)
    ratio_combobox = create_custom_combobox(frame, row=4, column=3, options=ratio_options, default_value=ratio_initial)
    power_combobox = create_custom_combobox(frame, row=5, column=3, options=power_options, default_value=power_initial)

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
    keypad_button = ttk.Button(frame, text="Keypad", command=lambda: open_keypad(None))
    keypad_button.grid(row=6, column=4, pady=(25, 15), columnspan=1)

    # Create a text widget to display the output
    output_text = tk.Text(frame, bg="black", fg="white")
    output_text.grid(row=7, column=0, columnspan=8, pady=(15,0), padx=(30,20), sticky="nsew")

    # Bind the function to close open lists to the left mouse click event on the root window
    frame.bind("<Button-1>", lambda event: close_open_lists(event, frame))

