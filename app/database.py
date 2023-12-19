from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQL_DATABSE_URL = "postgresql://<name>:<password>@<ip_addr/hostname>:<port>/database_name"
SQL_DATABASE_URL = "postgresql://postgres:postgres@localhost/fastapi"

engine = create_engine(SQL_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()