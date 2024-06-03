import logging
import os

logging.basicConfig(
    format="| RTC-LOG |: %(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(os.path.join(os.getcwd(), 'system.log')),
              logging.StreamHandler()],
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.INFO,
)

UVC_LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': "%(asctime)s - %(levelname)s - %(message)s",
            'use_colors': True,
            'datefmt': '%d-%b-%y %H:%M:%S'
        },
        'access': {
            '()': 'uvicorn.logging.AccessFormatter',
            'use_colors': True,
            'fmt': '%(asctime)s - %(levelname)s - %(client_addr)s - "%(request_line)s" - %(status_code)s ',
            'datefmt': '%d-%b-%y %H:%M:%S'
        },
    },
    'handlers': {
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
        },
        'access': {
            'formatter': 'access',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(os.getcwd(), 'system.log'),
            'encoding': 'utf-8',
            'formatter': 'default',
        }
    },
    'loggers': {
        'uvicorn': {'handlers': ['default', 'file'], 'level': 'INFO', 'propagate': False},
        'uvicorn.error': {'level': 'INFO'},
        'uvicorn.access': {'handlers': ['access', 'file'], 'level': 'INFO', 'propagate': False},
        'gunicorn.error': {'handlers': ['default'], 'level': 'INFO', 'propagate': False},
        'gunicorn.access': {'handlers': ['access'], 'level': 'INFO', 'propagate': False},
    },
}



