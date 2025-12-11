import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_reset_code_email(recipient_email: str, code: str):
    subject = "Your Password Reset Code"
    body = f"""
    Hello,

    You requested to reset your password.
    Your 6-digit verification code is: {code}

    This code will expire in 10 minutes.

    Regards,
    Support Team
    """

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
