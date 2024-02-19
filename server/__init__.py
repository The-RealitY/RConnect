import os

import uvicorn

from server import com
from server import model

from server.__main__ import Base, engine, app
from server.util.logger import UVC_LOGGING_CONFIG

# Create tables
Base.metadata.create_all(bind=engine)
server_port = int(os.getenv('PORT', '8000'))

config = uvicorn.Config(app, host="0.0.0.0", port=server_port, log_config=UVC_LOGGING_CONFIG, reload=True)
