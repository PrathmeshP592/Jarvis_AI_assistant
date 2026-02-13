import os
import numpy as np
import sounddevice as sd
from piper.voice import PiperVoice

BASE_DIR = os.path.dirname(__file__)

VOICE_MODEL = os.path.join(BASE_DIR, "en_US-lessac-medium.onnx")
VOICE_CONFIG = os.path.join(BASE_DIR, "en_US-lessac-medium.onnx.json")

voice = PiperVoice.load(VOICE_MODEL, VOICE_CONFIG)


import os
import numpy as np
import sounddevice as sd
from piper.voice import PiperVoice

BASE_DIR = os.path.dirname(__file__)

VOICE_MODEL = os.path.join(BASE_DIR, "en_US-lessac-medium.onnx")
VOICE_CONFIG = os.path.join(BASE_DIR, "en_US-lessac-medium.onnx.json")

voice = PiperVoice.load(VOICE_MODEL, VOICE_CONFIG)


# def speak(text):
#     print("🔊 Jarvis speaking...")

#     audio_chunks = []

#     for chunk in voice.synthesize(text):
#         audio_chunks.append(chunk.audio_float_array)

#     if not audio_chunks:
#         print("⚠ No audio generated")
#         return

#     audio = np.concatenate(audio_chunks)

#     sd.play(audio, samplerate=chunk.sample_rate)
#     sd.wait()

def speak(text):
    print("🔊 Jarvis speaking...")

    audio_chunks = []

    for chunk in voice.synthesize(text):
        audio_chunks.append(chunk.audio_float_array)

    if not audio_chunks:
        print("⚠ Piper returned silence, retrying...")
        for chunk in voice.synthesize(text):
            audio_chunks.append(chunk.audio_float_array)

    if not audio_chunks:
        print("❌ Still silent — skipping speech")
        return

    audio = np.concatenate(audio_chunks)

    sd.play(audio, samplerate=chunk.sample_rate)
    sd.wait()