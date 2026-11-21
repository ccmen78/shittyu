import json
import copy
from pathlib import Path

DATA_DIR = Path.home() / ".studyplan"
DATA_FILE = DATA_DIR / "data.json"

DEFAULT_DATA = {
    "term_end_date": "",
    "assignments": [],
    "courses": [],
    "prev_gpa": 0.0,
    "prev_credits": 0.0,
    "study_minutes": 0
}


def load_data():
    """
    Load local data.
    Return default data if file does not exist
    or contains invalid JSON.
    """

    if not DATA_FILE.exists():
        return copy.deepcopy(DEFAULT_DATA)

    try:

        with open(
            DATA_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        # Ensure all required fields exist
        for key in DEFAULT_DATA:

            data.setdefault(
                key,
                DEFAULT_DATA[key]
            )

        return data

    except (
        json.JSONDecodeError,
        FileNotFoundError
    ):

        return copy.deepcopy(DEFAULT_DATA)


def save_data(data):
    """
    Save data to local JSON file.
    """

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    try:

        with open(
            DATA_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
