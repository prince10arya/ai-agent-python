import os
from langchain.chat_models import init_chat_model


GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise NotImplementedError("`GROQ_API_KEY` is required")




def get_openai_llm():
    model = init_chat_model("llama-3.1-8b-instant", model_provider="groq")
    return model
