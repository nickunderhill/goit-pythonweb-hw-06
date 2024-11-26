from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/student_db",
)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
