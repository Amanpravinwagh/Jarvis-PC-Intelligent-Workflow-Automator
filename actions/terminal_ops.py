import subprocess
import os
import shlex
import threading

def run_command(cmd: str, shell=False):
    """
    Run a command in a new terminal window on Windows.
    For cross-platform adaptation, modify this function.
    """
    try:
        if os.name == "nt":  # Windows
            # spawn a new cmd window
            subprocess.Popen(["powershell", "-NoExit", "-Command", cmd])
        else:
            # for linux/mac open a new terminal (best-effort)
            subprocess.Popen(shlex.split(cmd))
        return f"Started command: {cmd}"
    except Exception as e:
        return f"Failed to run command: {e}"

def start_timer(minutes: int):
    # Very simple non-blocking timer using a thread
    import time
    import threading

    def _timer(m):
        time.sleep(m * 60)
        # At end, we can ring TTS; keep it simple
        try:
            from speech.tts import speak
            speak(f"Timer finished: {m} minutes")
        except Exception:
            print("Timer finished.")
    t = threading.Thread(target=_timer, args=(minutes,), daemon=True)
    t.start()
    return f"Timer started for {minutes} minutes."
