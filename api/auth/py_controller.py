
from sqlalchemy.orm.session import Session
from api.user.email_config import setting
import pandas as pd
from random import randint
from api.user.models import Users
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from api.utils.db_utils import database
from api.Deep_fake import conf

def check_user_exist(email,engine):
    query = 'select * from USERS where email='+"'"+str(email)+"'"
    df= pd.read_sql(query,engine)
    return df.shape[0]

# def email_config_data():
#     return email_config.setting()
def generate_code():
    return randint(100000,1000000)

async def send_auth_code(email):
    passcode = generate_code()
    print (passcode)
    query = "Update users set passcode='" + str(passcode) + "'where email='"+ str(email)+"'"
    print(email)
    print(query)
    await database.execute(query)
    return passcode

def generate_register_email(RECEIVER_EMAIL):
    subject = "Verification Code"
    body ="\nHi Mate,\n\n Thanks For Register Yourself With Us \n\n <h1> Explore The New World Of DeepFake With Us <h1>"
    sender_email = conf.EMAIL_ID
    #email_config().email_id
    receiver_email = RECEIVER_EMAIL
    password = conf.EMAIL_PWD
    #email_config().email_pwd

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

def generate_login_email(RECEIVER_EMAIL):
    subject = "URGENT: Login With New Device"
    body ="\nHi User,\n\n We Noticed That You logged in Your Account \n If it isn't you Kindly change your pasword"
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

#previous
def generate_auth_email(passcode1,RECEIVER_EMAIL):
    subject = "Verification Code"
    body ="\nHi Everyone,\n\n Your verification code is "+str(passcode1)
    sender_email = conf.EMAIL_ID
    #email_config().email_id
    receiver_email = RECEIVER_EMAIL
    password = conf.EMAIL_PWD
    #email_config().email_pwd

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

def generate_password_change_email(RECEIVER_EMAIL):
    subject = "URGENT: Password Change"
    body ="\nHi User,\n\n Your password changed successfully "
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


def validate_passcode(email,passcode,engine):
    query = "select * from USERS WHERE EMAIL='"+str(email)+"' AND PASSCODE = "+str(passcode)
    df=pd.read_sql(query,engine)
    if df.shape[0]>0:
        return True
    else:
        return False

async def update_password(email,password):
    #query = "UPDATE USERS SET PASSWORD ='" + str(password) + "' where EMAIL='" + str(email) + "'"
    print(username)
    query = Users.__table__.update().where(Users.username == username).values(
            password = util.get_password_hash(password),
            passcode = 000000
    )
    print(query)
    await database.execute(query)