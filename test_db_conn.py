from sqlalchemy import create_engine
import os

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost/employee_db"

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'connect_timeout': 5})
    with engine.connect() as connection:
        print("Successfully connected to the database!")
except Exception as e:
    print(f"Error connecting to the database: {e}")
