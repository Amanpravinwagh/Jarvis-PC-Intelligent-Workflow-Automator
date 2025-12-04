import json
import os
from tinydb import TinyDB, Query

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
WORKFLOW_FILE = os.path.join(BASE_DIR, "data", "workflows.json")

def load_workflows():
    if not os.path.exists(WORKFLOW_FILE):
        return {}
    with open(WORKFLOW_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_workflow(name: str, actions: list):
    wf = load_workflows()
    wf[name] = {
        "name": name,
        "actions": actions
    }
    with open(WORKFLOW_FILE, "w", encoding="utf-8") as f:
        json.dump(wf, f, indent=2)

def parse_command_to_actions(text: str):
    """
    Simple rule-based parser mapping text into actions.
    This is intentionally small so you can expand.
    """
    text = text.lower().strip()
    workflows = load_workflows()

    # direct workflow trigger
    if text.startswith("start ") or text.startswith("run "):
        # e.g., "start coding mode" => look for "coding mode" in workflows by fuzzy match
        for name, wf in workflows.items():
            if name in text or name.replace("_", " ") in text:
                return {"task": name, "actions": wf["actions"]}
    # basic commands
    actions = []
    if "study" in text or "study mode" in text:
        if "study_setup" in workflows:
            return {"task": "study_setup", "actions": workflows["study_setup"]["actions"]}
        # fallback
        actions.append({"type": "open_website", "value": "https://drive.google.com"})
        actions.append({"type": "open_folder", "value": "C:\\Users\\%USERNAME%\\Documents\\MBA_PDFs"})
        actions.append({"type": "start_timer", "value": 45})
        return {"task": "study_mode", "actions": actions}

    if "coding" in text or "code" in text or "coding mode" in text:
        actions.append({"type": "open_app", "value": "cursor"})
        actions.append({"type": "open_app", "value": "code"})  # fallback open VSCode
        actions.append({"type": "open_folder", "value": "C:\\Users\\%USERNAME%\\projects"})
        actions.append({"type": "run_command", "value": "powershell -NoExit -Command \"conda activate myenv\""})
        return {"task": "coding_mode", "actions": actions}

    if "clean my downloads" in text or "clean downloads" in text:
        actions.append({"type": "sort_downloads", "value": None})
        return {"task": "clean_downloads", "actions": actions}

    if text.startswith("open ") and "website" not in text:
        # open app or folder
        words = text.split()
        target = " ".join(words[1:])
        actions.append({"type": "open_app", "value": target})
        return {"task": "open", "actions": actions}

    # fallback: no match
    return {"task": "unknown", "actions": []}
