"""
Author: Humanpredator
Note: Main file to run the server
"""
import os
import subprocess
import sys

import uvicorn

from server import ENGINEE, MODEL, SERVER_PORT, app, ALEMBIC_DIR, DB_URI, LOGGER
# noinspection PyUnresolvedReferences
from server import model, com
from server.util.logger import UVC_LOGGING_CONFIG

# Server startup and shutdown handler modify as your need.
app.add_event_handler('startup', lambda: LOGGER.info("Starting API Server!"))
app.add_event_handler('shutdown', lambda: LOGGER.info("Shutting API Server!"))


# Run DB migrate on every server startup.
def run_migration():
    # Initialize Alembic if it hasn't been initialized
    if not os.path.exists(ALEMBIC_DIR):
        subprocess.run(['alembic', 'init', ALEMBIC_DIR])
        # Configure alembic.ini
        with open('alembic.ini', 'r') as file:
            nw_config = file.read()
        nw_config = nw_config.replace('driver://user:pass@localhost/dbname', DB_URI)
        with open('alembic.ini', 'w') as file:
            file.write(nw_config)
        # Update alembic/env.py to import models and set target_metadata
        env_path = os.path.join(ALEMBIC_DIR, 'env.py')
        with open(env_path, 'r') as file:
            env_content = file.read()
        env_content = env_content.replace(
            'target_metadata = None',
            'from server.model import *\n'
            'from server import MODEL\n'
            'target_metadata = MODEL.metadata'
        )
        with open(env_path, 'w') as file:
            file.write(env_content)

    LOGGER.info('\n<-------------Running Migration-------------->')
    subprocess.run([sys.executable, '-m', 'alembic', 'revision', '--autogenerate', '-m', 'Server Startup Migration!'])
    subprocess.run([sys.executable, '-m', 'alembic', 'upgrade', 'head'])
    LOGGER.info('\n<-------------Migration Completed-------------->')


if __name__ == "__main__":
    run_migration()
    MODEL.metadata.create_all(bind=ENGINEE)
    config = uvicorn.Config(app, host="0.0.0.0", port=SERVER_PORT, log_config=UVC_LOGGING_CONFIG)
    uvicorn.Server(config).run()
