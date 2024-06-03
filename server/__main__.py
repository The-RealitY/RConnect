import uvicorn
from server import ENGINEE, MODEL, SERVER_PORT,app
# Create tables
from server import com
from server import model
from server.util.logger import UVC_LOGGING_CONFIG

MODEL.metadata.create_all(bind=ENGINEE)

app.add_event_handler('startup', lambda: print("API Server Startup"))
app.add_event_handler('shutdown', lambda: print("API Server Shutdown"))

if __name__ == "__main__":
    config = uvicorn.Config(app, host="0.0.0.0", port=SERVER_PORT, log_config=UVC_LOGGING_CONFIG, reload=True)
    uvicorn.Server(config).run()