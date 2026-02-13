from faster_whisper import WhisperModel
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

# Force CPU mode (no CUDA, no crashes)
model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

SAMPLE_RATE = 16000


def listen(duration=6):
    print("🎤 Listening... speak naturally")

    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"
    )
    sd.wait()

    wav.write("input.wav", SAMPLE_RATE, audio)

    segments, _ = model.transcribe("input.wav")

    text = " ".join(seg.text for seg in segments).strip()

    return text
