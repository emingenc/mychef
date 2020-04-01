import os

from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL")

# connect engine to database and create all tables
engine = create_engine(DATABASE_URL)

# create and configure "Session" to be used throughout app
Session = sessionmaker(bind=engine)
session = Session()

database = Database(DATABASE_URL)
