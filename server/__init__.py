"""
Author: Humanpredator
Note: Initialization file where all configuration from config.env file will be loaded
"""
import logging
import os
import sys
import time

from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from server.util.cryptograph import CryptoSecure
from server.util.quickresponse import GenerateQRC
from fastapi.middleware.cors import CORSMiddleware


SERVER_UPTIME = time.time()
# Load the config from config.env
if not os.path.exists('config.env'):
    print("config.env file doesn't exist on the directory, please refer the README to set up configuration, existing!")
    sys.exit(1)
load_dotenv('config.env')
app = FastAPI()

# Allow All Origin Request
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["http://localhost:3000"],  
)

# Create DB con and session
MODEL = declarative_base()
DB_URI = os.getenv('DATABASE_URI')
ENGINEE = create_engine(DB_URI)
SESSION = sessionmaker(autocommit=False, autoflush=False, bind=ENGINEE)

# Other Config
CIPHER = CryptoSecure(os.getenv('SECRET_KEY', 'password'))
QRCG = GenerateQRC(os.getenv('QRC_PATH', 'qrc'))
SERVER_PORT = int(os.getenv('PORT', '8000'))
LOGGER = logging.getLogger(__name__)
ALEMBIC_DIR = 'alembic'

# System Verification either auto or manual
AUTO_VERIFY = True if str(os.getenv('AUTO_VERIFY', 'true')).lower() == 'true' else False
SMTP_SERVER = os.getenv('SMTP_SERVER', None)
SMTP_PORT = os.getenv('SMTP_PORT', None)
SMTP_LOGIN = os.getenv('SMTP_LOGIN', None)
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', None)
SMTP_SENDER = os.getenv('SMTP_SENDER', None)
