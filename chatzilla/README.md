# chatzilla

This package is for a python interface to interact with a local LLaMA instance. 
One can send requests to a local instance of [ollama](https://ollama.com/)

Provides a simple and intuitive way to send prompts, start conversations, 
and retrieve chat histories.

## Classes
- `ChatOllama`: Initialize a chat with local ollama instance.
    - Parameters: `ollama_url`, `model`
    - Methods:
        - `begin(content, role, json_output)`: Start a chat with a large language model (llm) with a given prompt
        - `next(content, json_output)`: Continue the chat with the same llm, while including chat history
        - `history()`: Return the current chat history as a list

## Functions
  - `PromptOllama(prompt, model, ollama_url, format, json_output)`
          Send a single prompt to ollama without any history
  - `zillaping(ollama_url)`
          Ping local instance of ollama to see if the sever is running