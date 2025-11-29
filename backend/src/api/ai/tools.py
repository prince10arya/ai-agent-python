"""AI tools module for LangChain tool definitions.

Provides LangChain-compatible tools that AI agents can use to:
- Send emails
- Read inbox
- Research and generate email content
"""

from langchain_core.tools import tool

from api.myemailer.sender import send_mail
from api.myemailer.myinbox_reader import read_inbox
from api.ai.services import generate_email_message


@tool
def send_me_email(subject: str, content: str) -> str:
    """Send an email with the given subject and content.
    
    This tool allows AI agents to send emails via SMTP.
    Used by agents to execute email sending operations.
    
    Args:
        subject: Email subject line
        content: Email body content (plain text)

    Returns:
        str: "sent email" if successful, "Not Sent" if failed
        
    Example:
        >>> result = send_me_email("Meeting Reminder", "Don't forget our meeting at 3pm")
        >>> print(result)
        "sent email"
    """
    try:
        # Attempt to send email via SMTP
        send_mail(subject=subject, content=content)
    except:
        # Return failure message if any error occurs
        return "Not Sent"
    return "sent email"


@tool
def get_unread_emails(hours_ago: int = 48) -> str:
    """Retrieve unread emails from the inbox.
    
    Fetches unread emails from the specified time period and formats
    them as text. HTML content is removed for cleaner output.
    
    Args:
        hours_ago: Number of hours to look back for emails (default: 48)

    Returns:
        str: Formatted string of email data separated by dashes,
             or error message if retrieval fails
             
    Example:
        >>> emails = get_unread_emails(24)
        >>> print(emails)
        "from: john@example.com\tsubject: Meeting\n-----\n..."
    """
    try:
        # Read emails from inbox within specified timeframe
        emails = read_inbox(hours_ago=hours_ago, verbose=False)
    except:
        return "Error getting latest emails"
    
    # Clean and format email data
    cleaned = []
    for email in emails:
        data = email.copy()
        # Remove HTML body to reduce clutter
        if "html_body" in data:
            data.pop('html_body')
        # Format email fields as key-value pairs
        msg = ""
        for k, v in data.items():
            msg += f"{k}:\t {v}"
        cleaned.append(msg)
    
    # Join all emails with separator
    return "\n-----\n".join(cleaned)


@tool
def research_email(query: str) -> str:
    """Research a topic and generate email content.
    
    Uses AI to research the given topic and generate a complete
    email with subject and body content.
    
    Args:
        query: Research topic or email description
               (e.g., "product launch announcement")
    
    Returns:
        str: Formatted email with subject and body
        
    Example:
        >>> result = research_email("quarterly business update")
        >>> print(result)
        "Subject: Q4 Business Update\n Body: Dear Team, I wanted to share..."
    """
    # Generate email content using AI
    response = generate_email_message(query=query)
    
    # Format as readable email string
    msg = f"Subject {response.subject}: \n Body: {response.content}"
    return msg
