import re
import openai
from audio import listen_to_voice
from gpt import gpt_response
from speech import speak_text
from utils import log_error
from webBrowser import open_web_browser
from file_dialog import handle_file_selection
from file_voice import handle_voice_file_selection
from text_file_handler import handle_create_text_file  

command_patterns = {
    re.compile(r'\bopen disney plus\b', re.IGNORECASE): lambda command: open_web_browser("https://www.disneyplus.com/"),
    re.compile(r'\bopen netflix\b', re.IGNORECASE): lambda command: open_web_browser("https://www.netflix.com/"),
    re.compile(r'\bselect file\b', re.IGNORECASE): handle_file_selection,
    re.compile(r'\bopen file\b', re.IGNORECASE): handle_voice_file_selection,
    re.compile(r'\bcreate text file\b', re.IGNORECASE): handle_create_text_file,
}

def main():
    openai_key = input("Please enter your OpenAI secret key: ")
    trigger_word = "chief"
    print("Starting main loop...")
    while True:
        try:
            voice_input = listen_to_voice()
            if voice_input:
                print(f"Voice input received: {voice_input}")
                if trigger_word in voice_input.lower():
                    # Extract the command after the trigger word
                    command_part = voice_input.lower().split(trigger_word, 1)[1].strip()
                    print(f"Command part after trigger word: {command_part}")
                    
                    # Find the command handler or use the default GPT-4 response
                    handled = False
                    for pattern, handler in command_patterns.items():
                        match = pattern.search(command_part)
                        if match:
                            command = command_part[match.end():].strip()
                            handler(command, openai_key)
                            handled = True
                            break
                    if not handled:
                        response = gpt_response(voice_input, openai_key)
                        print(f"GPT-4 says: {response}")
                        speak_text(response)
                elif voice_input.lower() == "goodbye":
                    speak_text("Goodbye")
                    break
        except Exception as e:
            print(f"An error occurred in the main loop: {e}")
            log_error(e)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An unhandled exception occurred: {e}")
        log_error(e)
