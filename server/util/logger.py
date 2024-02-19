import os
from typing import Any

UVC_LOGGING_CONFIG: dict[str, Any] = {
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
    },
}
