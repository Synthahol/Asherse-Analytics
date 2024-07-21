# email_utils.py
from flask import current_app as app
from flask_mail import Message

from app import mail


def send_email(subject, recipients, body):
    msg = Message(subject=subject, recipients=recipients)
    msg.body = body
    try:
        mail.send(msg)
        return True, "Email sent successfully"
    except Exception as e:
        app.logger.error(f"Error sending email: {e}")
        return False, str(e)
