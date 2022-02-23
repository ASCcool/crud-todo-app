from xmlrpc.client import DateTime
from sqlalchemy import Column, Integer, String, Date
from database import Base

# Define To Do class inheriting from Base
class ToDo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    task = Column(String(256))
    due_date = Column(Date)
    is_completed = Column(String(256))
    assigned_to = Column(String(256))
