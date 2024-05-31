import tkinter as tk
from tkinter import ttk

def clear_console():
    """Clears the console."""
    output_text.delete("1.0", tk.END)

def show_waiting_message():
    """Function to display a waiting message in the console."""
    clear_console()
    output_text.insert(tk.END, "Waiting for response from server...\n")
    output_text.see(tk.END)
    output_text.update_idletasks()

def create_custom_combobox(frame, row, column, options, default_value):
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
    combobox_entry.insert(0, default_value
