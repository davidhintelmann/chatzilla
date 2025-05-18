# LLaMify + chatzilla

Query local ollama instance to explore the world of open source large language models.
Provides a simple and intuitive way to send prompts, start conversations, 
and retrieve chat histories.

<!-- ![overview](docs/imgs/<image>.png) -->

Checkout the `demo.ipynb` jupyter notebook to get a quick demo on the capabilties of this library.

## Take a Gander

- Jump into `demo/chat.py` to extend an ongoing conversation.
- chatzilla folder is the package developed as shown below.

## Features 

- Send single prompts or start conversations
- Continue conversations while including chat history
- Retrieve chat history and assistant responses

## Installation

clone this repository and install the requirements with:

```pwsh
pip install -r requirements.txt
```

use the following command to point your chat requests to ollama's api endpoint

```python
from dotenv import load_dotenv

load_dotenv()
ollama_url = os.getenv("OLLAMA_CHAT") # http://localhost:11434/api/chat   
```

**Recommend:** create a python virtual environment first. 

If you haven't done this before, please check the python [docs](https://docs.python.org/3/library/venv.html) for more information.

## Usage

### Single Prompt

Use the `PromptOllama` function to send a single prompt to LLaMA.

```python
from chatzilla import PromptOllama

response = PromptOllama("What do you call a fake noodle?", "llama3.1")
print(response)  # prints "An impasta!"
```

#### Conversation

Use the `ChatOllama` class to start and continue conversations.

```python
from chatzilla import ChatOllama

chat = ChatOllama("Hello!", "llama3.1")
response = chat.begin()
print(response)  # prints "How are you today?"

next_response = chat.next("I'm good, thanks!")
print(next_response)  # prints something like a continuation of the conversation
```

#### Chat History

Use the `history` method to retrieve the current chat history.

```python
print(chat.history()) # prints list of chat history, example below: 
# [     
#   {"role": "user", "content": "Hello!"},
#   {"role": "assistant", "content": "How are you today?"} 
# ]
```