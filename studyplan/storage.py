# studyplan/storage.py
import json
from pathlib import Path

DATA_DIR = Path.home() / ".studyplan"
DATA_FILE = DATA_DIR / "data.json"

DEFAULT_DATA = {
    "term_end_date": "",
    "assignments": [],
    "courses": [],
    "prev_gpa": 0.0,
    "prev_credits": 0.0
}

def load_data():
    """Load local data, return default data if not exists."""
    if not DATA_FILE.exists():
        return DEFAULT_DATA.copy()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return DEFAULT_DATA.copy()

def save_data(data):
    """Save data to local JSON file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
