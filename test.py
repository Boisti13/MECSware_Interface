import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle

# Create the main window
root = tk.Tk()
root.title("Custom Combobox Dropdown")
root.geometry("300x200")

# Create a list of options
options = ["Option 1", "Option 2", "Option 3", "Option 4"]

# Create a combobox-like entry widget
combobox_entry = ttk.Entry(root)
combobox_entry.grid(row=0, column=0, padx=10, pady=10)

# Create a Listbox to act as the dropdown list
listbox = tk.Listbox(root, font=('TkDefaultFont', 20), width=20)
for option in options:
    listbox.insert(tk.END, option)

# Function to handle item selection
def select_item(event):
    selected_item = listbox.get(listbox.curselection())
    combobox_entry.delete(0, tk.END)
    combobox_entry.insert(0, selected_item)
    listbox.place_forget()

# Bind the selection event to the Listbox
listbox.bind("<<ListboxSelect>>", select_item)

# Function to show/hide the dropdown list
def toggle_dropdown():
    if listbox.winfo_ismapped():
        listbox.place_forget()
    else:
        listbox.place(x=combobox_entry.winfo_x(), y=combobox_entry.winfo_y() + combobox_entry.winfo_height())

# Create a button to toggle the dropdown list
dropdown_button = ttk.Button(root, text="▼", command=toggle_dropdown)
dropdown_button.grid(row=0, column=1, padx=(0, 10))

# Start the main event loop
root.mainloop()