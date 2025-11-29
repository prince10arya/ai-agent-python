import os
import smtplib
from email.message import EmailMessage


EMAIL= os.environ.get("EMAIL")
APP_PASSWORD= os.environ.get("APP_PASSWORD")
EMAIL_HOST=os.environ.get("EMAIL_HOST") or 'smtp.gmail.com'
EMAIL_PORT=os.environ.get("EMAIL_PORT") or 465

def send_mail(subject: str, content: str, to_email: str, from_email: str = EMAIL):
    msg = EmailMessage()
    msg["Subject" ] = subject
    msg["From" ] = from_email
    msg["To" ] = to_email
    msg.set_content(content)
    try:
        # Connect to Gmail's SMTP server using SSL on port 465
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL, APP_PASSWORD)
            smtp.send_message(msg)
        print(f"Email sent successfully from {from_email} to {to_email} using SSL.")
    except smtplib.SMTPAuthenticationError:
        print("Authentication Error: Check your email and app password.")
        print("For Gmail, ensure you're using an App Password if 2FA is enabled.")
    except smtplib.SMTPConnectError as e:
        print(f"SMTP Connection Error: {e}")
        print("Check if the SMTP host and port are correct and reachable.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


