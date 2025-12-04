import os
import shutil
import time
from pathlib import Path

DOWNLOADS = os.path.join(os.path.expanduser("~"), "Downloads")

EXT_MAP = {
    "images": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"],
    "documents": [".pdf", ".docx", ".doc", ".txt", ".pptx", ".ppt", ".xlsx"],
    "videos": [".mp4", ".mov", ".mkv", ".webm"],
    "archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "code": [".py", ".ipynb", ".js", ".java", ".cpp", ".c", ".cs"]
}

def safe_move(src: str, dst: str):
    os.makedirs(dst, exist_ok=True)
    base = os.path.basename(src)
    dst_path = os.path.join(dst, base)
    # avoid overwrite
    if os.path.exists(dst_path):
        name, ext = os.path.splitext(base)
        dst_path = os.path.join(dst, f"{name}_{int(time.time())}{ext}")
    shutil.move(src, dst_path)

def sort_downloads(target_dir=DOWNLOADS, days_old=None):
    if not os.path.exists(target_dir):
        return f"No downloads folder at {target_dir}"
    moved = 0
    for entry in os.scandir(target_dir):
        if entry.is_file():
            ext = os.path.splitext(entry.name)[1].lower()
            moved_to = None
            for cat, exts in EXT_MAP.items():
                if ext in exts:
                    dst = os.path.join(target_dir, cat.capitalize())
                    safe_move(entry.path, dst)
                    moved += 1
                    moved_to = dst
                    break
            if not moved_to:
                dst = os.path.join(target_dir, "Other")
                safe_move(entry.path, dst)
                moved += 1
    return f"Sorted {moved} files from Downloads."

def clean_old_files(target_dir=DOWNLOADS, older_than_days=60):
    cutoff = time.time() - older_than_days * 86400
    removed = 0
    for root, dirs, files in os.walk(target_dir):
        for name in files:
            path = os.path.join(root, name)
            if os.path.getmtime(path) < cutoff:
                try:
                    os.remove(path)
                    removed += 1
                except:
                    pass
    return f"Removed {removed} old files older than {older_than_days} days."
