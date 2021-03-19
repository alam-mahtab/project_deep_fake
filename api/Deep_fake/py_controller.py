from sqlalchemy.orm.session import Session
from api.user.email_config import setting
from api.utils import email_utils
import pandas as pd
from random import randint
from api.user import models
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from . import conf
def check_user_exist(email,engine):
    query = 'select * from USERS where email='+"'"+str(email)+"'"
    df= pd.read_sql(query,engine)
    return df.shape[0]

def generate_uploading_email(RECEIVER_EMAIL):
    subject = "URGENT: Your Request Is Received"
    body ="\nHi User,\n\n Your request is logged in our system \n\n you will receive another email when work is done "
    sender_email = conf.EMAIL_ID
    receiver_email = RECEIVER_EMAIL
    password = conf.EMAIL_PWD

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