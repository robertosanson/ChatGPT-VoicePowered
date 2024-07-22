import tkinter as tk
from tkinter import filedialog
from speech import speak_text
from utils import log_error
import os
import platform

root = tk.Tk()
root.withdraw() 

def handle_file_selection(command=None):
    try:
        file_path = filedialog.askopenfilename()
        if file_path:
            speak_text(f"You have selected the file: {file_path}")
            print(f"File selected: {file_path}")
            open_file(file_path)

        else:
            speak_text("No file was selected")
            print("No file selected")
    except Exception as e:
        print(f"Error selecting file: {e}")
        log_error(e)

def open_file(file_path):
    try:
        if platform.system() == 'Windows':
            os.startfile(file_path)
        elif platform.system() == 'Darwin':  # macOS
            os.system(f'open "{file_path}"')
        else:  # Linux and other OSes
            os.system(f'xdg-open "{file_path}"')
        print(f"File opened: {file_path}")
    except Exception as e:
        print(f"Error opening file: {e}")
        log_error(e)