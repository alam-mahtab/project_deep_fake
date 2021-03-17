from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, Sequence
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
    


