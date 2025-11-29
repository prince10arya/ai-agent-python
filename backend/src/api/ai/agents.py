"""AI agents module for email management.

Provides LangGraph-based AI agents with tool-calling capabilities
for email operations like sending, reading, and researching.
"""

from langgraph.prebuilt import create_react_agent
from api.ai.llms import get_openai_llm
from api.ai.tools import (send_me_email, get_unread_emails, research_email)


# Dictionary mapping tool names to their implementations
EMAIL_TOOLS = {
    "send_me_email": send_me_email,
    "get_unread_emails": get_unread_emails
}


def send_email_agent():
    """Create an AI agent for email sending operations.
    
    Creates a ReAct agent that can generate and send emails using
    the send_me_email tool. The agent can understand natural language
    requests and execute email sending operations.
    
    Returns:
        Agent: LangGraph ReAct agent configured for email sending
        
    Example:
        >>> agent = send_email_agent()
        >>> result = agent.invoke({"messages": [{"role": "user", 
        ...     "content": "Send thank you email to john@example.com"}]})
    """
    # Get LLM model instance
    model = get_openai_llm()
    
    # Create ReAct agent with email sending tool
    agent = create_react_agent(
        model=model,
        tools=[send_me_email],
        prompt="You are a helpful assistant for managing my email inbox for "
               "generating, sending and reviewing emails"
    )
    return agent


def get_research_agent():
    """Create an AI agent for email research and preparation.
    
    Creates a ReAct agent that can research topics and prepare
    email content using the research_email tool.
    
    Returns:
        Agent: LangGraph ReAct agent configured for email research
        
    Example:
        >>> agent = get_research_agent()
        >>> result = agent.invoke({"messages": [{"role": "user",
        ...     "content": "Research about product launch announcement"}]})
    """
    # Get LLM model instance
    model = get_openai_llm()
    
    # Create ReAct agent with research tool
    agent = create_react_agent(
        model=model,
        tools=[research_email],
        prompt="You are a helpful research assistant for preparing email data",
        name='research_agent'
    )
    return agent
