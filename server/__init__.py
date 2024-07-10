"""
Author: Humanpredator
Note: Initialization file where all configuration from config.env file will be loaded
"""
import logging
import os
import time

from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from server.util.cryptograph import CryptoSecure
from server.util.quickresponse import GenerateQRC

# Load the config from config.env
load_dotenv('config.env')
app = FastAPI()

# Create DB con and session
MODEL = declarative_base()
DB_URI = os.getenv('DATABASE_URI')
ENGINEE = create_engine(DB_URI)
SESSION = sessionmaker(autocommit=False, autoflush=False, bind=ENGINEE)

# Other Config
CIPHER = CryptoSecure(os.getenv('SECRET_KEY', 'password'))
QRCG = GenerateQRC(os.getenv('QRC_PATH', 'qrc'))
SERVER_PORT = int(os.getenv('PORT', '8000'))
SERVER_UPTIME = time.time()
LOGGER = logging.getLogger(__name__)
ALEMBIC_DIR = 'alembic'

# System Verification either auto or manual
AUTO_VERIFY = True if str(os.getenv('AUTO_VERIFY', 'true')).lower() == 'true' else False
SMTP_SERVER = os.getenv('SMTP_SERVER', None)
SMTP_PORT = os.getenv('SMTP_PORT', None)
SMTP_LOGIN = os.getenv('SMTP_LOGIN', None)
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', None)
SMTP_SENDER = os.getenv('SMTP_SENDER', None)
