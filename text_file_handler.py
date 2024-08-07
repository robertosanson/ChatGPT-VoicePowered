import os
from speech import speak_text
from utils import log_error
from gpt import gpt_response

def handle_create_text_file(command, openai_key):
    try:
        command_parts = command.split(' ', 1)
        if len(command_parts) < 2:
            speak_text("Please provide a file name and a prompt for the text file.")
            return

        file_name, prompt = command_parts
        file_name = file_name.strip() + ".txt"
        prompt = prompt.strip()

        content = gpt_response(prompt, openai_key)

        save_path = os.path.join(os.getcwd(), file_name)

        with open(save_path, 'w') as file:
            file.write(content)

        speak_text(f"Text file '{file_name}' has been created with the generated content.")
        print(f"Text file '{file_name}' has been created with the generated content.")

    except Exception as e:
        print(f"Error creating text file: {e}")
        log_error(e)
        speak_text("There was an error creating the text file.")
