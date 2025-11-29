"""Email sender module for SMTP operations.

Handles sending emails via Gmail SMTP server with SSL encryption.
Requires Gmail App Password for authentication.
"""

import os
import smtplib
from email.message import EmailMessage

# Load email configuration from environment variables
EMAIL = os.environ.get("EMAIL")  # Sender email address
APP_PASSWORD = os.environ.get("APP_PASSWORD")  # Gmail App Password
EMAIL_HOST = os.environ.get("EMAIL_HOST") or 'smtp.gmail.com'  # SMTP server
EMAIL_PORT = os.environ.get("EMAIL_PORT") or 465  # SSL port


def send_mail(subject: str, content: str, to_email: str, from_email: str = EMAIL):
    """Send an email via Gmail SMTP server.
    
    Connects to Gmail's SMTP server using SSL on port 465 and sends
    an email with the specified subject and content.
    
    Args:
        subject: Email subject line
        content: Email body content (plain text)
        to_email: Recipient email address
        from_email: Sender email address (defaults to EMAIL env var)
        
    Raises:
        SMTPAuthenticationError: If email/password authentication fails
        SMTPConnectError: If connection to SMTP server fails
        Exception: For any other unexpected errors
        
    Example:
        send_mail(
            subject="Hello",
            content="This is a test email",
            to_email="recipient@example.com"
        )
    """
    # Create email message object
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content(content)
    
    try:
        # Establish secure SSL connection to Gmail SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            # Authenticate with Gmail credentials
            smtp.login(EMAIL, APP_PASSWORD)
            # Send the email message
            smtp.send_message(msg)
        print(f"Email sent successfully from {from_email} to {to_email} using SSL.")
        
    except smtplib.SMTPAuthenticationError:
        # Handle authentication failures (wrong email/password)
        print("Authentication Error: Check your email and app password.")
        print("For Gmail, ensure you're using an App Password if 2FA is enabled.")
        raise
        
    except smtplib.SMTPConnectError as e:
        # Handle connection failures (network/server issues)
        print(f"SMTP Connection Error: {e}")
        print("Check if the SMTP host and port are correct and reachable.")
        raise
        
    except Exception as e:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred: {e}")
        raise


