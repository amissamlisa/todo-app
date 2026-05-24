import ssl
from smtplib import SMTP
from email.mime.text import MIMEText
from email.utils import formatdate
from backend.config import settings


def create_mime_text(from_email, to_email, message, subject):
    msg = MIMEText(message, "plain", "utf-8")

    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Date"] = formatdate()

    return msg


def send_email(from_email, to_email, message, subject):
    msg = create_mime_text(from_email, to_email, message, subject)
    SMTP_HOST = settings.SMTP_HOST
    SMTP_PORT = settings.SMTP_PORT
    SMTP_USERNAME = settings.SMTP_USERNAME
    SMTP_PASSWORD = settings.SMTP_PASSWORD

    context = ssl.create_default_context()
    server = SMTP(SMTP_HOST, SMTP_PORT)
    try:
        server.starttls(context=context)
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
    finally:
        server.quit()
