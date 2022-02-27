from xmlrpc.client import DateTime
from sqlalchemy import Column, Integer, String, Date, Boolean
from database import Base, Users

class ToDo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    task = Column(String(256))
    due_date = Column(Date)
    is_completed = Column(String(256))
    assigned_to = Column(String(256))
    created_by = Column(String(256))
    group_name = Column(String(256))

class User(Users):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(256))
    password = Column(String(256))
    email = Column(String(256))
    full_name = Column(String(256))