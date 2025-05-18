import json
import pathlib
import logging
import datetime
from typing import List, Dict, Literal

# Define the root of your repo (adjust if needed)
REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent # Adjust based on project structure

class RepoRelativePathFormatter(logging.Formatter):
    """custom logging formatter used in `logger_init` function for consistent 
    relative path to trace where the logging message was executed from"""
    def format(self, record):
        full_path = pathlib.Path(record.pathname).resolve()
        try:
            record.relpath = str(full_path.relative_to(REPO_ROOT))
        except ValueError:
            # Path not relative to repo (e.g., external library), fallback to filename
            record.relpath = record.filename
        return super().format(record)

def logger_init(format:str='%(asctime)s | %(levelname)-8s | %(relpath)s:%(lineno)4d | %(message)s') -> logging.Logger:
    """
    initialize the python logger
    
    logging format = '%(asctime)s | %(levelname)-8s | %(relpath)s:%(lineno)4d | %(message)s'

    Example
    ---
    format is outputted to the console in the following format:

    2025-05-18 14:26:12,391 | INFO     | LLaMify\tst.py:  28 | <message>
    """
    # Use custom formatter with default StreamHandler
    handler = logging.StreamHandler()
    handler.setFormatter(RepoRelativePathFormatter(format))

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False
    return logger

def save_history_to_json(history: List[Dict[Literal['user'] | Literal['assistant'], str]], print_filepath:bool=False) -> str:
    """
    Utility function to save chat history to a json file.

    - Creates two folders if they do not exist. 
        - A folder name `results` if it does not already exist (**note**: this folder is ignored via .gitignore). 
        - Inside results, a daily folder is also created and has the following naming convention: `MM_DD_YY` e.g., 05_18_2025 
    - Inside the daily folder chat histories are saved as `.json` files.
        - This file has the following naming convention: `run_HH-MM-SS.json` e.g., run_03-37-54.json

    Parameters
    ---
    history : list
        this is the message history obtained from `PromptOllama` or `ChatOllama` classes
    print_filepath : bool, default=False
        set to True for printing the filepath to the console

    Returns
    ---
    This method returns a string for the filepath where the json file was saved

    Example
    ---
    json file will have the following structure:
    
    ```python
    [
        {
            "role": "user",
            "content": "describe how to use llama3.1 to create an agentic workflow using a reAct approach."
        },
        {
            "role": "assistant",
            "content": "Llama 3.1 is a powerful tool for automating workflows, and the reactive (reAct) approach is a great way to build flexible and scalable systems. To create an agentive workflow using a reAct approach with ..."
        },
        {
            "role": "user",
            "content": "if you do not know what llama3.1 can you search webpages to find out?"
        },
        {
            "role": "assistant",
            "content": "I don't have any prior knowledge about Llama 3.1, but I can try to find information on the web ..."
        },
        {
            "role": "user",
            "content": "do you know about ollama for self deployment of large language models?"
        },
        {
            "role": "assistant",
            "content": "I think I can try to find some information on OLLAMA!..."
        }
    ]
    ```
    """
    now = datetime.datetime.now()

    # Determine this script's parent directory
    script_dir = pathlib.Path(__file__).resolve().parent
    results_dir = script_dir.parent / "results" / now.strftime("%m_%d_%Y")

    results_dir.mkdir(parents=True, exist_ok=True)

    filename = f"run_{now.strftime('%H-%M-%S')}.json"
    output_path = results_dir / filename

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

    if print_filepath:
        print(f"file saved at: {output_path}\tfilename: {filename}")
    
    return output_path