
from api.ai.llms import get_openai_llm
from api.ai.schemas import EmailMessage


def generate_email_message(query: str) -> EmailMessage:
    llm_base = get_openai_llm()
    llm = llm_base.with_structured_output(EmailMessage)
    messages = [
    (
        "system",
        "You are a helpful assistant for research and composing plaintext emails. Do not use markdown in your response only use plain text."
    ),
    ("human", f"{query}"),
    ]
    return llm.invoke(messages)
