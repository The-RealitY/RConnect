import uvicorn

from server import config

if __name__ == "__main__":

    uvicorn.Server(config).run()

