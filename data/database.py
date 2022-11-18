from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://a123:4231@localhost:5432/test_project"
SQLALCHEMY_DATABASE_BACKUP_URL = "postgresql://a123:4231@localhost:5433/test_project_backup"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


engine_backup = create_engine(
    SQLALCHEMY_DATABASE_BACKUP_URL,
    pool_pre_ping=True
)
SessionLocalBackup = sessionmaker(autocommit=False, autoflush=False, bind=engine_backup)


Base = declarative_base()
