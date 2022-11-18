import time

from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session

from data import crud, models, schemas
from data.database import SessionLocal, SessionLocalBackup, engine, engine_backup
from data.errors import TransactionError


models.Base.metadata.create_all(bind=engine)
models.Base.metadata.create_all(bind=engine_backup)

app = FastAPI()
DATABASE_ENABLED = True


def get_db():
    db = SessionLocal() if DATABASE_ENABLED else SessionLocalBackup()
    try:
        yield db
    finally:
        db.close()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    global DATABASE_ENABLED
    db_main = SessionLocal()
    try:
        db_main.execute('SELECT 1')
        print("db is working")
        if not DATABASE_ENABLED:
            db = SessionLocalBackup()
            crud.restore_transactions(db_main, db, True)
            DATABASE_ENABLED = True
            db.close()
            print("db is reseted")
    except Exception as e:
        print("db is not working")
        DATABASE_ENABLED = False
    finally:
        db_main.close()
    return await call_next(request)


@app.post("/transaction/{user_id}")
async def transaction(user_id: int, data: schemas.Transaction, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None and DATABASE_ENABLED:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        if DATABASE_ENABLED:
            if db_user.balance + data.value < 0:
                raise HTTPException(status_code=409, detail="Not enough money")
            else:
                crud.create_transaction(db, user_id, data.value)
                crud.add_balance_value(db, db_user.id, data.value)
                return {"balance": db_user.balance}
        else:
            crud.create_transaction(db, user_id, data.value)
            return {"balance": "unknown"}

    except TransactionError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
