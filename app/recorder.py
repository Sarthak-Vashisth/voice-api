import requests
import speech_recognition as sr
import threading
import uuid
from datetime import datetime


recognizer = sr.Recognizer()
mic = sr.Microphone()
audio_data = None

def listen():
    global audio_data
    with mic as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening... Press Enter to stop recording.")
        audio_data = recognizer.listen(source, phrase_time_limit=None)

def wait_for_enter():
    input()
    print("Stopping recording...")

def listen_and_split_words():
    listener_thread = threading.Thread(target=listen)
    stopper_thread = threading.Thread(target=wait_for_enter)

    listener_thread.start()
    stopper_thread.start()

    stopper_thread.join()
    if listener_thread.is_alive():
        print("Please wait while the last sentence finishes...")
        listener_thread.join()

    if audio_data:
        try:
            print("Recognizing speech...")
            sentence = recognizer.recognize_google(audio_data)
            words = sentence.split()
            data = {
            "user_id": "Sarthak",
            "session_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "sentence": sentence,
            "words": words
        }
            res = requests.post("http://127.0.0.0:5000/store", json=data)
            print("Response:", res.json())
        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
    else:
        print("No audio captured.")

if __name__ == "__main__":
    listen_and_split_words()

