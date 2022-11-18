import decimal
import time

import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import func

import data.models as models
from data.errors import TransactionError


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_transaction(db: Session, user_id: int, income: int, time=None):
    order = db.query(func.max(models.UserTransaction.order).filter(models.UserTransaction.user_id == user_id)).scalar()
    if order is None:
        order = 0

    db_transaction = models.UserTransaction(user_id=user_id,
                                            order=order + 1,
                                            income=income,
                                            time=time)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def add_balance_value(db: Session, user_id: int, income: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        db_user = models.User(id=user_id, balance=0)
        db.add(db_user)
    db_user.balance = db_user.balance + income
    db.commit()
    db.refresh(db_user)
    return db_user


def restore_transactions(db_main: Session, db_backup: Session, clean: bool = False):
    for user in db_main.query(models.User):
        for trans in db_backup.query(models.UserTransaction).filter(models.UserTransaction.user_id == user.id):
            if user.balance + trans.income >= 0:
                create_transaction(db_main, user.id, trans.income, trans.time)
    if clean:
        db_backup.execute("delete from user_transaction")
        db_backup.commit()
