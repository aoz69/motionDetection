# Import the tkinter library for creating the GUI window and functions for file dialogs.
import tkinter as tk
from tkinter import filedialog
from functions import use_video_file, use_webcam

# Define a function to create the graphical user interface (GUI) elements.
def create_gui(root):
    # Set the title of the main application window.
    root.title("Motion Detection")

    # Create a button labeled "Use Video File" and assign the use_video_file function as its command.
    video_file_button = tk.Button(root, text="Use Video File", command=use_video_file)
    video_file_button.pack(pady=10)  # Add some spacing for better visual appearance.

    # Create a button labeled "Use Webcam" and assign the use_webcam function as its command.
    webcam_button = tk.Button(root, text="Use Webcam", command=use_webcam)
    webcam_button.pack(pady=10)  # Add some spacing for better visual appearance.
