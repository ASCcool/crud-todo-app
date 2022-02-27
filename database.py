from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///todo.db")

engine1 = create_engine("sqlite:///users.db")

Base = declarative_base(bind=engine)

Users = declarative_base(bind=engine1)