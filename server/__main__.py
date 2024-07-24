"""
Author: Humanpredator
Note: Main file to run the server
"""
import os
import subprocess
import sys
import re
import uvicorn
from sqlalchemy import text

from server import ENGINEE, MODEL, SERVER_PORT, app, ALEMBIC_DIR, DB_URI, LOGGER, SESSION
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

    # Configure alembic.ini
    with open('alembic.ini', 'r') as file:
        old_config = file.read()
    nw_config = re.sub(
        r'^sqlalchemy\.url\s*=\s*.*$',  # Pattern to match the sqlalchemy.url line
        f'sqlalchemy.url = {DB_URI}',  # Replacement line
        old_config,  # Content to search
        flags=re.MULTILINE  # Make sure the pattern matches line by line
    )
    with open('alembic.ini', 'w') as file:
        file.write(nw_config)
    with SESSION() as session:
        session.execute(text("DROP TABLE IF EXISTS alembic_version;"))
        session.commit()
    LOGGER.info('\n<-------------Running Migration-------------->')
    subprocess.run([sys.executable, '-m', 'alembic', 'revision', '--autogenerate', '-m', 'Startup Migration!'])
    subprocess.run([sys.executable, '-m', 'alembic', 'upgrade', 'head'])
    LOGGER.info('\n<-------------Migration Completed-------------->')


if __name__ == "__main__":
    MODEL.metadata.create_all(bind=ENGINEE)
    run_migration()
    config = uvicorn.Config(app, host="0.0.0.0", port=SERVER_PORT, log_config=UVC_LOGGING_CONFIG)
    uvicorn.Server(config).run()
