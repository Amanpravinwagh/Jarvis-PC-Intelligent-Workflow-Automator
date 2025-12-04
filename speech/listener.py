import queue
import sounddevice as sd
import json
import os
from vosk import Model, KaldiRecognizer

# Listener that returns text for a spoken input (single-shot)
# Requires a Vosk model downloaded locally. See README for link.

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model")

def load_model(model_path: str):
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Vosk model not found at {model_path}. Download a small model and put it there. See README."
        )
    return Model(model_path)

def listen_once(timeout=10, model_path=MODEL_PATH, device=None, samplerate=16000):
    model = load_model(model_path)
    rec = KaldiRecognizer(model, samplerate)
    q = queue.Queue()

    def callback(indata, frames, time, status):
        q.put(bytes(indata))

    with sd.RawInputStream(samplerate=samplerate, blocksize = 8000, dtype='int16',
                           channels=1, callback=callback, device=device):
        print("Listening... speak now.")
        text = ""
        try:
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get("text", "")
                    break
        except KeyboardInterrupt:
            pass
    if not text:
        # Try final partial
        final = json.loads(rec.FinalResult())
        text = final.get("text", "")
    print("Recognized:", text)
    return text
