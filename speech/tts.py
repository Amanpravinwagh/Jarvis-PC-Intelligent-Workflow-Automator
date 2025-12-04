import pyttsx3
import threading
import queue

engine = pyttsx3.init()
tts_queue = queue.Queue()

def _tts_worker():
    while True:
        text = tts_queue.get()
        engine.say(text)
        engine.runAndWait()
        tts_queue.task_done()

worker_thread = threading.Thread(target=_tts_worker, daemon=True)
worker_thread.start()

def speak(text, block=True):
    tts_queue.put(text)
    if block:
        tts_queue.join()
