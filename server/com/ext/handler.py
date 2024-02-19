from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from uvicorn.config import logger

from server.__main__ import app, session

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*,"],  # Allow all origins, replace with specific domains in production
    allow_credentials=True,
    allow_methods=["*,"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*,"]  # Allow all headers
)


# Http Error Code handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "data": [],
            "message": (
                f"Failed Endpoint: {request.url}\n"
                f"Failed Method: {request.method}\n"
                f"Failed Reason {str(exc.detail).strip()!r}"
            )
        },
    )


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            request.state.db = session()
            response = await call_next(request)
            return response
        except Exception as e:
            request.state.db.rollback()

            logger.error(f"\n<<<---Start of Exception---\n{str(e)}\n---End of Exception--->")
            return JSONResponse(
                status_code=500,
                content={
                    "data": [],
                    "message": (
                        f"Failed Endpoint: {request.url} \n"
                        f"Failed Method: {request.method} \n"
                        f"Failed Reason {str(e).strip()!r}"
                    )
                },
            )
        finally:
            request.state.db.close()


app.add_middleware(ExceptionMiddleware)


# On Event Function
@app.on_event('shutdown')
async def on_exit():
    print("HERE")
