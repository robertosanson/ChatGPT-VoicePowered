import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import tempfile
import numpy as np
import queue
import time
from utils import log_error

recognizer = sr.Recognizer()
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    q.put(indata.copy())

def record_audio(fs=44100, chunk_size=1024, threshold=0.01, silence_duration=2.0):
    print("Starting audio recording...")
    try:
        with sd.InputStream(samplerate=fs, channels=1, callback=callback, blocksize=chunk_size):
            print("Speak now...")
            silence_start = None
            frames = []
            recording = True
            while recording:
                while not q.empty():
                    frame = q.get()
                    frames.append(frame)
                    audio_data = np.concatenate(frames, axis=0)
                    rms = np.sqrt(np.mean(audio_data[-chunk_size:]**2))  
                    print(f"RMS: {rms}")
                    if rms < threshold:
                        if silence_start is None:
                            silence_start = time.time()
                            print("Silence started at:", silence_start)
                        elif time.time() - silence_start > silence_duration:
                            print("Silence detected, stopping recording.")
                            recording = False
                            break
                    else:
                        if silence_start is not None:
                            print("Speech detected, resetting silence_start.")
                        silence_start = None
                sd.sleep(100)
            if frames:
                audio_data = np.concatenate(frames, axis=0)
                print(f"Audio data length: {len(audio_data)}")
                return audio_data, fs
            else:
                print("No audio data captured.")
                return None, None
    except Exception as e:
        print(f"Error recording audio: {e}")
        log_error(e)
        return None, None

def save_audio(audio, filename, fs):
    try:
        sf.write(filename, audio, fs)
        print(f"Audio saved to {filename}.")
    except Exception as e:
        print(f"Error saving audio: {e}")
        log_error(e)

def listen_to_voice():
    print("Listening for your voice...")
    audio, fs = record_audio()
    if audio is None or len(audio) == 0:
        print("No audio data captured.")
        return ""

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio_file:
            save_audio(audio, temp_audio_file.name, fs)
            with sr.AudioFile(temp_audio_file.name) as source:
                audio_data = recognizer.record(source)
                print("Recognizing...")
                try:
                    text = recognizer.recognize_google(audio_data)
                    print(f"You said: {text}")
                    return text
                except sr.UnknownValueError:
                    print("Could not understand the audio")
                    return ""
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
                    log_error(e)
                    return ""
    except Exception as e:
        print(f"Error processing audio: {e}")
        log_error(e)
        return ""
