# Import the tkinter library for creating a GUI.
import tkinter as tk

# Import the create_gui function from the gui.py file.
from gui import create_gui

# Check if this script is the main entry point.
if __name__ == "__main__":
    # Create a Tkinter root window, which serves as the main window of the GUI application.
    root = tk.Tk()

    # Call the create_gui function to create the user interface and pass the root window as an argument.
    create_gui(root)

    # Start the Tkinter main event loop, which keeps the GUI running until the user closes the window.
    root.mainloop()
