"""
chatzilla

A Python interface to interact with a local LLaMA instance.

Provides a simple and intuitive way to send prompts, start conversations,
and retrieve chat histories from a local LLaMA instance.

Features:
    - Send single prompts or start conversations
    - Continue conversations while including chat history
    - Retrieve chat history and assistant responses

Installation:
    clone this repository and install the requirements with:

    pip install -r requirements.txt

    Recommend: create a python virtual environment first.

Usage:
    To use ollama, import it into your Python script and use its classes and functions.
    See below for examples:

    >>> from chatzilla import PromptOllama
    >>> response = PromptOllama("What do you call a fake noodle?", "llama3.1")
    >>> print(response)  # prints "An impasta!"

    >>> from chatzilla import ChatOllama
    >>> chat = ChatOllama("Hello!", "llama3.1")
    >>> response = chat.begin()
    >>> print(response)  # prints "How are you today?"

    >>> next_response = chat.next("I'm good, thanks!")
    >>> print(next_response)  # prints something like a continuation of the conversation

Classes:
    - `ChatOllama`: Initialize a chat with local ollama instance.
        - Parameters: `ollama_url`, `model`
        - Methods:
            - `begin(content, role, json_output)`: Start a chat with a large language model (llm) with a given prompt
            - `next(content, json_output)`: Continue the chat with the same llm, while including chat history
            - `history()`: Return the current chat history as a list

Functions:
    - `PromptOllama(prompt, model, ollama_url, json_output)`
            Send a single prompt to ollama without any history
    - `zillaping(ollama_url, model, role)`
            Ping local instance of ollama to see if the sever is running
"""
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException
from json import dumps
from typing import List, Dict, Literal, Union, Optional
from .logger import logger_init

logger = logger_init()

def zillaping(ollama_url:str) -> Optional[str]:
    """
    Ping local instance of ollama to see if the sever is running

    Parameters
    ---
    ollama_url : str
        endpoint for local instance of ollama (e.g., 'http://localhost:11434')

    Returns
    ---
    str or None
        When the server is running then the string `Ollama is running` is returned. 
        Otherwise None is returned and an exception is logged: 
        - ConnectionError
        - Timeout
        - RequestException
    """
    try:
        response = requests.get(ollama_url, timeout=5)
        return response.text
    except ConnectionError as e:
        logger.error(f"ConnectionError occurred while requesting {ollama_url}: {e}")
        return None
    except Timeout as e:
        logger.error(f"Timeout error occurred while requesting {ollama_url}: {e}")
        return None
    except RequestException as e:
        logger.error(f"RequestException error occurred while requesting {ollama_url}: {e}")
        return None

def PromptOllama(prompt:str, model:str, ollama_url:str, json_output:bool=False) -> str | Dict[str, Union[str, int, float, bool]]:
    """
    Send a single prompt to ollama without any history
    
    Parameters
    ---
    prompt: str
        user input for prompt (Q&A, summarize, etc.)
    model: str
        model installed with local instance of ollama (e.g., 'llama3.1')
    ollama_url: str
        API endpoint for local instance of ollama (e.g., 'http://localhost:11434/api/generate')
    json_output: bool
            By default, only return the assistant response from ollama. 
            Set to `True` in order to return the entire json response from ollama

    Returns
    ---
    This method will return either a string from the http post response or json depending on `json_output` parameter.

    default `json_output=False`

        "Here's one: What do you call a fake noodle? An impasta!"

    set `json_output=True`
    ```python
    {
        'model': 'llama3.1',
        'created_at': '2025-05-17T19:31:35.0504806Z',
        'response': "Here's one: What do you call a fake noodle? An impasta!",
        'done': True,
        'done_reason': 'stop',
        'context': [128006, 882, 128007, 271, 73457, 757, 264, 22380, 128009, 128006, 78191, 128007, 271, 8586, 596, 832, 1473, 3923, 656, 499, 1650, 264, 12700, 46895, 273, 1980, 2127, 3242, 14635, 0],
        'total_duration': 609726400,
        'load_duration': 25319400,
        'prompt_eval_count': 14,
        'prompt_eval_duration': 1073400,
        'eval_count': 18,
        'eval_duration': 582819100
    }
    ```
    """
    h = {"Content-Type":"application/json"}
    d = {
        "model":model,
        "prompt":prompt,
        "stream":False
    }
    response = requests.post(ollama_url, headers=h, data=dumps(d))
    if not json_output:
        return response.json()['response']
    else:
        return response.json()

class ChatOllama:
    """
    Initialize a chat with a local ollama instance.

    Parameters
    ---
    ollama_url : str
        API endpoint for local instance of ollama (e.g., ollama_url='http://localhost:11434/api/chat')

    model : str, default='llama3.1'
        select model installed with ollama

    Methods
    ---
    - begin
        Start a chat with a large language model (llm) with a given prompt

    - next
        Continue the chat with the same llm, while including chat history

        
    """
    def __init__(self, ollama_url:str, model:str="llama3.1"):
        self.url = ollama_url
        self.model = model
        self.chat_history = []

    def begin(self, content:str, role:str="user", json_output:bool=False) -> str | Dict[str, Union[str, int, float, bool, Dict[str, str]]]:
        """
        Start a chat with a large language model (llm) with given a prompt

        Parameters
        ---
        content : str
            prompt for beginning the conversation
        
        role : str, default='user'
            this chat bot allows 'user', 'assistant', 'system', and 'tool' roles
            - user is the prompt input
            - assistant is the llm response output
            - system will take priority over user
            - tool is for creating a tool call

        json_output : bool, default=False
            By default, only return the assistant response from ollama. 
            Set `json_output=True` to return the entire json response from ollama

        Return
        ---
        this method will return either a string from the http post response or json depending on `json_output` parameter.

        default `json_output=False`

            "Here's one: What do you call a fake noodle? An impasta!"

        set `json_output=True`
        ```python
        {
            'model': 'llama3.1',
            'created_at': '2025-05-17T19:56:23.4930816Z',
            'message': {
                'role': 'assistant',
                'content': 'The salary for this job offer is a range of $85,500 - $114,000 per annum.'
            },
            'done_reason': 'stop',
            'done': True,
            'total_duration': 575025300,
            'load_duration': 17167900,
            'prompt_eval_count': 1643,
            'prompt_eval_duration': 6156600,
            'eval_count': 23,
            'eval_duration': 551174400
        }
        ```
        """
        h = {"Content-Type":"application/json"}
        d = {
            "model":self.model,
            "messages": [{
                "role": role, 
                "content": content
            }],
            "stream":False
        }

        self.chat_history.append({"role": role, "content": content})

        response_json = requests.post(self.url, headers=h, data=dumps(d)).json()
        response_text = response_json['message']['content']

        self.chat_history.append({"role": "assistant", "content": response_text})

        if not json_output:
            return response_text
        else:
            return response_json
    
    def next(self, content:str, json_output:bool=False) -> str | Dict[str, Union[str, int, float, bool]]:
        """
        Continue the chat with the same llm, while including chat history

        Parameters
        ---
        json_output: bool
            By default, only return the assistant response from ollama. 
            Set to `True` in order to return the entire json response from ollama

        Return
        ---
        this method will return either a string from the http post response or json depending on `json_output` parameter.

        default `json_output=False`

            "Here's one: What do you call a fake noodle? An impasta!"

        set `json_output=True`
        ```python
        {
            'model': 'llama3.1',
            'created_at': '2025-05-17T19:31:35.0504806Z',
            'response': "Here's one: What do you call a fake noodle? An impasta!",
            'done': True,
            'done_reason': 'stop',
            'context': [128006, 882, 128007, 271, 73457, 757, 264, 22380, 128009, 128006, 78191, 128007, 271, 8586, 596, 832, 1473, 3923, 656, 499, 1650, 264, 12700, 46895, 273, 1980, 2127, 3242, 14635, 0],
            'total_duration': 609726400,
            'load_duration': 25319400,
            'prompt_eval_count': 14,
            'prompt_eval_duration': 1073400,
            'eval_count': 18,
            'eval_duration': 582819100
        }
        ```
        """
        h = {"Content-Type":"application/json"}
        self.chat_history.append({"role": "user", "content": content})
        d = {
            "model":self.model,
            "messages": self.chat_history,
            "stream":False
        }
        response_json = requests.post(self.url, headers=h, data=dumps(d)).json()
        response_text = response_json['message']['content']
        self.chat_history.append({"role": "assistant", "content": response_text})
        if not json_output:
            return response_text
        else:
            return response_json
    
    def history(self) -> List[Dict[Literal['user'] | Literal['assistant'], str]]:
        """
        Return the current chat history as a list

        Return
        ---
        list of chat history, example below:

        ```python
        [
            {"role": "user", "content": "blah blah blah"},
            {"role": "assistant", "content": "yada yada yada"},
            ...
        ]
        ```
        """
        return self.chat_history
