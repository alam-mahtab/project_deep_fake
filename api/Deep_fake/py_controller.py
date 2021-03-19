from sqlalchemy.orm.session import Session
from api.user.email_config import setting
from api.user import email_config
import pandas as pd
from random import randint
from api.user import models
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def generate_uploading_email(RECEIVER_EMAIL):
    subject = "URGENT: Password Change"
    body ="\nHi User,\n\n Your password changed successfully "
    sender_email = email_config().email_id
    receiver_email = RECEIVER_EMAIL
    password = email_config().email_pwd

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_email)
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtpout.secureserver.net", 465, context=context) as server:
    #with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)