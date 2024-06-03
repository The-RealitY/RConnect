import logging
import os
import sys
import time

from dotenv import load_dotenv
from fastapi import FastAPI
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from server.util.cryptograph import CryptoSecure
from server.util.quickresponse import GenerateQRC

load_dotenv('config.env')
app = FastAPI()

# Configure database connection
MODEL = declarative_base()
ENGINEE = create_engine(os.getenv('DATABASE_URI'))
SESSION = sessionmaker(autocommit=False, autoflush=False, bind=ENGINEE)

# Other Config
CIPHER = CryptoSecure(os.getenv('SECRET_KEY', 'password'))
QRCG = GenerateQRC(os.getenv('QRC_PATH', 'qrc'))
SERVER_PORT = int(os.getenv('PORT', '8000'))
SERVER_UPTIME = time.time()
LOGGER = logging.getLogger(__name__)
