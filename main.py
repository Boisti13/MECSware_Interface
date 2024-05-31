import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle
from PIL import Image, ImageTk
from ui_setup import setup_ui
from event_handlers import setup_event_handlers

def main():
    # Create the main window
    root = tk.Tk()
    root.title("MECSware Interface")
    root.geometry("800x600")  # Initial size of the window

    # Set the theme for the application
    style = ThemedStyle(root)
    style.set_theme("adapta")  # Replace "adapta" with your desired theme

    # Create the main frame with padding
    frame = ttk.Frame(root, padding="20")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    for i in range(8):
        frame.columnconfigure(i, weight=1)

    # Configure row and column weights to allow resizing
    frame.grid_rowconfigure(7, weight=1)  # Row containing the output_text widget
    frame.grid_columnconfigure(0, weight=1)

    # Load and display the logo image
    try:
        image = Image.open("/home/pi/Desktop/MECSware_GUI/logo.png")
        image = image.convert("RGBA")  # Ensure the image has an alpha channel for transparency
        image_resized = image.resize((180, 70), Image.ANTIALIAS)
        logo = ImageTk.PhotoImage(image_resized)
        logo_label = tk.Label(frame, image=logo, bg="ghost white")
        logo_label.grid(row=0, column=6, rowspan=2, columnspan=2)  # Adjust the position as needed
    except Exception as e:
        messagebox.showerror("Error", f"Unable to load image: {e}")

    # Setup UI elements and event handlers
    setup_ui(frame)
    setup_event_handlers(root, frame)

    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()
