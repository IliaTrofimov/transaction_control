from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, ForeignKey, func
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    balance = Column(Integer)


class UserTransaction(Base):
    __tablename__ = "user_transaction"

    user_id = Column(Integer, primary_key=True)
    order = Column(Integer, primary_key=True)
    income = Column(Integer)
    time = Column(DateTime, server_default=func.now())
