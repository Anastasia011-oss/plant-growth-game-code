import json
import os

SAVE_FILE = "save_backup.json"

def save_game(data: dict):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_game():
    if not os.path.exists(SAVE_FILE):
        return None
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
