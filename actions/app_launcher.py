import os
import subprocess
import webbrowser
import shlex
import sys

# Config: map friendly names to paths/commands. Adapt to your system.
APP_MAP = {
    "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "code": "C:\\Users\\%USERNAME%\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
    "cursor": "C:\\Users\\%USERNAME%\\AppData\\Local\\Programs\\CursorAI\\Cursor.exe",
    "notepad": "notepad.exe",
    "powershell": "powershell.exe"
}

def open_app(name: str):
    name = name.lower().strip()
    # direct path?
    if os.path.exists(name):
        os.startfile(name)
        return f"Opened {name}"
    # map lookup
    exe = APP_MAP.get(name)
    if exe:
        path = os.path.expandvars(exe)
        try:
            os.startfile(path)
            return f"Opened {name}"
        except Exception:
            subprocess.Popen([path])
            return f"Opened {name}"
    # try system open
    try:
        subprocess.Popen(shlex.split(name))
        return f"Opened {name}"
    except Exception as e:
        return f"Failed to open {name}: {e}"

def open_website(url: str):
    if not url.startswith("http"):
        url = "https://" + url
    webbrowser.open(url)
    return f"Opened website {url}"
