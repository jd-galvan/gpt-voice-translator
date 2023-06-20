from playsound import playsound
from gtts import gTTS
from scipy.io.wavfile import write
import sounddevice as sd

import openai

import os
from getkey import getkey, key
from dotenv import load_dotenv

load_dotenv()

while True:
    print("Presiona ENTER si quieres decir algo")
    k = getkey()
    if k != key.ENTER:
        break

    print("Grabando...")
    # Recording
    fs = 44100  # Sample rate
    seconds = 5  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    write('input.mp3', fs, myrecording)  # Save file

    print("Traduciendo...")
    playsound("waiting.mp3")

    # Translate
    openai.api_key = os.environ.get("GPT_ACCESS_KEY")
    audio_file = open("input.mp3", "rb")
    response = openai.Audio.translate("whisper-1", audio_file)
    print(f"Traducción: {response['text']}")

    t1 = gTTS(response["text"], lang="en")
    t1.save("output.mp3")
    playsound("output.mp3")
