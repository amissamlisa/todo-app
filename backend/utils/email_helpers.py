import ssl
from smtplib import SMTP
from email.mime.text import MIMEText
from email.utils import formatdate


def create_mime_text(from_email, to_email, message, subject):
    msg = MIMEText(message, "plain", "utf-8")

    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Date"] = formatdate()

    return msg


def send_email(from_email, to_email, message, subject, account_name, password):
    msg = create_mime_text(from_email, to_email, message, subject)

    host = "smtp.gmail.com"
    port = 587

    context = ssl.create_default_context()
    server = SMTP(host, port)
    server.starttls(context=context)

    server.login(account_name, password)
    server.send_message(msg)
    server.quit()
