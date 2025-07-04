from langgraph.prebuilt import create_react_agent
from api.ai.llms import get_openai_llm
from api.ai.tools import ( send_me_email, get_unread_emails, research_email )




EMAIL_TOOLS= {
    "send_me_email": send_me_email,
    "get_unread_emails": get_unread_emails
}


def send_email_agent():
    model = get_openai_llm()
    agent = create_react_agent(
    model=model,
    tools=[send_me_email],
    prompt="You are a helpful assistant for managing my email inbox for generating, sending and reviewing emails"
    )
    return agent

def get_research_agent():
    model = get_openai_llm()
    agent = create_react_agent(
    model=model,
    tools=[research_email],
    prompt="You are a helpful research assistant for preparing email data",
    name='research_agent'
    )
    return agent
