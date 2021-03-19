from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, Sequence, ForeignKey
from sqlalchemy.orm import relationship
from api.utils.db_utils import Base
import datetime

metadata = MetaData()
# users = Table(
#     "py_user", metadata,
#     Column("id", Integer, primary_key = True), #, Sequence("user_id_seq")
#     Column("email",String(100)),
#     Column("phone",String(100)),
#     Column("password",String(100)),
#     Column("firstname",String(100)),
#     Column("lastname",String(100)),
#     Column("created_at",String(100)),
#     Column("status",String(1)),
# )
class Users(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True,unique=True)
    username = Column(String, unique=True)
    email = Column(String,unique=True)
    phone = Column(String)
    password = Column(String)
    firstname = Column(String)
    url = Column(String)
    lastname = Column(String)
    created_at = Column(DateTime,default=datetime.datetime.utcnow)
    status = Column(String)
    passcode = Column(String)
    deep_user = relationship('Fake',back_populates='client')
    #deep_make = relationship('Paid',back_populates='users')

# class Deep(Base):
#     __tablename__ = "deeps"

#     id = Column(Integer, primary_key=True,unique=True) 
#     created_at = Column(DateTime,default=datetime.datetime.utcnow)
#     url_photo = Column(String)
#     url_video = Column(String)
#     url_done = Column(String)
#     client_id = Column(String, ForeignKey('users.id'))
#     client = relationship('Users', back_populates='deep_user')

class Fake(Base):
    __tablename__ = "fakes"

    id = Column(Integer, primary_key=True) 
    created_at = Column(DateTime,default=datetime.datetime.utcnow)
    url_photo = Column(String)
    url_video = Column(String)
    url_done = Column(String)
    client_id = Column(String, ForeignKey('users.email'))
    client = relationship('Users', back_populates='deep_user')

