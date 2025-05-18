import sys
import os
from dotenv import load_dotenv
# Add the parent directory (llama-docx) to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from chatzilla import ChatOllama
from chatzilla.logger import logger_init, save_history_to_json

load_dotenv()
model = os.getenv("DEFAULT_MODEL") # llama3.1 8B
ollama_url = os.getenv("OLLAMA_CHAT") # http://localhost:11434/api/chat
logger = logger_init()
logger.info('Started')

# print(requests.get(checkURL).text)

conversations = {
    '1':[
        "describe how to use llama3.1 to create an agentic workflow using a reAct approach.",
        "if you do not know what llama3.1 can you search webpages to find out?",
        "do you know about ollama for self deployment of large language models?"
    ],
    '2':[
        "what llm are you?",
        "if you do not know what llama3.1 can you search webpages to find out?",
        "describe in great detail how you search webpages, are you requesting data right now or just using pretained data?"
    ],
    '3':[
        "which large language model are you?",
        "does ollama search webpages or do you need use a tool role",
        "describe in great detail how you search webpages, are you requesting data right now or just using pretained data?"
    ],
}

messages = conversations['3']

chat = ChatOllama(ollama_url, model) # do not need to insert model parameter here
_ = chat.begin(messages[0])
_ = chat.next(messages[1])
_ = chat.next(messages[2])

logger.info('Finished')
save_history_to_json(chat.history()) #saved to results folder, this folder is created if it does not already exist