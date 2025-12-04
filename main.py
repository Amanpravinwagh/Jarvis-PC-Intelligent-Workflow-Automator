import os
import json
import time
from pathlib import Path

from speech.tts import speak
from nlp.command_parser import parse_command_to_actions, load_workflows, save_workflow
from actions.app_launcher import open_app, open_website
from actions.file_ops import sort_downloads, clean_old_files
from actions.terminal_ops import run_command, start_timer

# OPTIONAL: import the STT listener if you set up Vosk. Otherwise fall back to text input.
try:
    from speech.listener import listen_once
    STT_AVAILABLE = True
except Exception:
    STT_AVAILABLE = False

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

def execute_action(action: dict):
    typ = action.get("type")
    val = action.get("value")
    if typ == "open_app":
        result = open_app(val)
    elif typ == "open_website":
        result = open_website(val)
    elif typ == "open_folder":
        # on windows os.startfile handles folders
        path = os.path.expandvars(val)
        if os.path.exists(path):
            os.startfile(path)
            result = f"Opened folder {path}"
        else:
            result = f"Folder not found: {path}"
    elif typ == "run_command":
        result = run_command(val)
    elif typ == "sort_downloads":
        result = sort_downloads()
    elif typ == "clean_old_files":
        days = action.get("days", 60)
        result = clean_old_files(older_than_days=days)
    elif typ == "start_timer":
        minutes = int(val) if val else 25
        result = start_timer(minutes)
    else:
        result = f"Unknown action type: {typ}"
    print(result)
    return result

def run_workflow(actions: list):
    speak("Executing workflow", block=False)
    for a in actions:
        execute_action(a)
    speak("Workflow complete.", block=False)

def interactive_record_workflow():
    """
    Simple recording mode. User triggers actions by typing commands while recording.
    For a richer recording mode you could monitor processes and file operations.
    """
    speak("Entering workflow recording mode. Type actions one per line, or 'done' to finish.")
    print("Recording actions. Supported action types:")
    print("open_app:<name>")
    print("open_website:<url>")
    print("open_folder:<path>")
    print("run_command:<command>")
    print("start_timer:<minutes>")
    actions = []
    while True:
        line = input("action> ").strip()
        if not line:
            continue
        if line.lower() in ("done", "exit", "stop"):
            break
        if ":" in line:
            typ, val = line.split(":", 1)
            actions.append({"type": typ.strip(), "value": val.strip()})
            print("Recorded:", typ, val)
        else:
            print("Invalid format. Use type:value")
    name = input("Enter workflow name to save: ").strip()
    save_workflow(name, actions)
    speak(f"Saved workflow {name}")
    print("Saved workflow:", name)

def main_loop():
    speak("Jarvis started. Say a command or type it.", block=False)
    while True:
        try:
            if STT_AVAILABLE:
                print("Say command or type 'type:' followed by text.")
                raw = input("Command (enter to use voice)> ").strip()
                if raw.lower().startswith("type:"):
                    command_text = raw[len("type:"):].strip()
                elif raw == "":
                    # use voice
                    command_text = listen_once()
                else:
                    command_text = raw
            else:
                raw = input("Type a command (or 'voice' if you set up Vosk)> ").strip()
                if raw.lower() == "voice":
                    print("Vosk not available. Install and place model in speech/model.")
                    command_text = ""
                else:
                    command_text = raw

            if not command_text:
                continue

            # special admin commands
            if command_text.lower() in ("exit", "quit"):
                speak("Goodbye", block=False)
                break
            if command_text.lower() in ("record workflow", "learn workflow", "record"):
                interactive_record_workflow()
                continue
            if command_text.lower().startswith("list workflows"):
                wfs = load_workflows()
                print("Workflows:", ", ".join(wfs.keys()))
                speak(f"I found {len(wfs)} workflows.", block=False)
                continue

            parsed = parse_command_to_actions(command_text)
            task = parsed.get("task")
            actions = parsed.get("actions", [])
            if task == "unknown" or not actions:
                speak("I did not understand the command. Try again or record a workflow.", block=False)
                print("Parsed:", parsed)
                continue

            speak(f"Executing {task}", block=False)
            run_workflow(actions)
            # here would be a good place to log usage to a DB or file
        except Exception as e:
            print("Error:", e)
            speak("An error occurred", block=False)

if __name__ == "__main__":
    main_loop()
