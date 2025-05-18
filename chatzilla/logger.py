import json
import pathlib
import logging
import datetime
from typing import List, Dict, Literal

# Define the root of your repo (adjust if needed)
REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent # Adjust based on project structure

class RepoRelativePathFormatter(logging.Formatter):
    def format(self, record):
        full_path = pathlib.Path(record.pathname).resolve()
        try:
            record.relpath = str(full_path.relative_to(REPO_ROOT))
        except ValueError:
            # Path not relative to repo (e.g., external library), fallback to filename
            record.relpath = record.filename
        return super().format(record)

def logger_init(format:str='%(asctime)s | %(levelname)-8s | %(relpath)s:%(lineno)4d | %(message)s'):
    # Use custom formatter with default StreamHandler
    handler = logging.StreamHandler()
    handler.setFormatter(RepoRelativePathFormatter(format))

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False
    return logger

def save_history_to_json(history: List[Dict[Literal['user'] | Literal['assistant'], str]]):
    now = datetime.datetime.now()

    # Determine this script's parent directory
    script_dir = pathlib.Path(__file__).resolve().parent
    results_dir = script_dir.parent / "results" / now.strftime("%m_%d_%Y")

    results_dir.mkdir(parents=True, exist_ok=True)

    filename = f"run_{now.strftime('%H-%M-%S')}.json"
    output_path = results_dir / filename

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

    print(f"file saved at: {output_path}\tfilename: {filename}")