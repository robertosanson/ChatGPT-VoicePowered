import os
import platform
from speech import speak_text
from utils import log_error

def handle_voice_file_selection(command):
    try:
        # Assuming the command contains the file name and file type
        root_path = "C:\\Users\\rober\\Documents\\"
        
        # Replace "space" and "underscore" with their respective characters
        command = command.replace(" space ", " ").replace(" underscore ", "_").replace(" dash ", "-")
        
        # Split the command into words
        words = command.split()
        if len(words) >= 2:
            file_name = " ".join(words[:-1])  # Join words with spaces
            file_type = words[-1]
            file_path = os.path.join(root_path, f"{file_name}.{file_type}")
            
            if os.path.isfile(file_path):
                speak_text(f"You have selected the file: {file_path}")
                print(f"File selected: {file_path}")
                open_file(file_path)
            else:
                speak_text(f"The specified file does not exist: {file_path}")
                print(f"The specified file does not exist: {file_path}")
        else:
            speak_text("Please specify both the file name and file type.")
            print("Command does not contain both file name and file type.")
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
