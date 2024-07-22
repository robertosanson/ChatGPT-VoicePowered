import pyttsx3
import random
from utils import log_error

tts_engine = pyttsx3.init()
voices = tts_engine.getProperty('voices')

greetings = [
    "Hi",
    "Hello there,",
    "Hey,",
    "Greetings,",
    "What's up,",
    "Hi there,",
    "Good day,"
]

def set_voice(voice_id):
    tts_engine.setProperty('voice', voice_id)
    tts_engine.setProperty('rate', 180)

def speak_text(text):
    try:
        set_voice(voices[1].id)  
        greeting = random.choice(greetings)
        tts_engine.say(f"{greeting} {text}")
        tts_engine.runAndWait()
        print("Text-to-speech completed.")
    except Exception as e:
        print(f"Error speaking text: {e}")
        log_error(e)
