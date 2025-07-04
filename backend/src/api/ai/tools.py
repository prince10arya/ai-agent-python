from langchain_core.tools import tool

from api.myemailer.sender import send_mail
from api.myemailer.myinbox_reader import read_inbox
from api.ai.services import generate_email_message

@tool
def send_me_email(subject: str, content: str) -> str:
    """_summary_

    Args:
        subject (str):
        content (str): 

    Returns:
        str: _description_
    """
    try:
        send_mail(subject=subject, content=content)
    except:
        return "Not Sent"
    return "sent email"


@tool
def get_unread_emails(hours_ago:int=48) -> str:
    """_summary_

    Args:
        hours_ago (int, optional): _description_. Defaults to 48.

    Returns:
        str: _description_
    """
    try:
        emails = read_inbox(hours_ago=hours_ago, verbose=False)
    except:
        return "Error getting latest emails"
    cleaned = []
    for email in emails:
        data = email.copy()
        if "html_body" in data:
            data.pop('html_body')
        msg = ""
        for k, v in data.items():
            msg += f"{k}:\t {v}"
        cleaned.append(msg)
    return "\n-----\n".join(cleaned)


@tool
def research_email(query: str):
    """Perform research based on the query

    Args:
        query (str): topic of research
    """
    response = generate_email_message(query=query)
    msg = f"Subject { response.subject}: \n Body: {response.content}"
    return msg
