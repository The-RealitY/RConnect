import os

from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from server.util.cryptograph import CryptoSecure
from server.util.quickresponse import GenerateQRC

load_dotenv('config.env')
app = FastAPI()

cipher = CryptoSecure(os.getenv('SECRET_KEY', 'password'))
qrc = GenerateQRC(os.getenv('QRC_PATH', 'qrc'))
# Configure database connection
Base = declarative_base()
engine = create_engine(os.getenv('DATABASE_URI'))
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

