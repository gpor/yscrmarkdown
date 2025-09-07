from langchain_ollama import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from dotenv import dotenv_values

env = dotenv_values(".env")

def embedding_model():
    if (ollama_embedding_model := env.get("OLLAMA_EMBEDDING_MODEL")) is not None:
        return OllamaEmbeddings(model=ollama_embedding_model)
    else:
        raise ValueError("embedding model not set in .env")


def llm():
    if (ollama_chat_model := env.get("OLLAMA_CHAT_MODEL")) is not None:
        return OllamaLLM(model=ollama_chat_model, keep_alive=3600)
    else:
        raise ValueError("chat model not set in .env")
