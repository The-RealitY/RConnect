import traceback

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from uvicorn.config import logger

from server import app, SESSION

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
                f"Failed Reason: {str(exc.detail).strip()!r}"
            )
        },
    )


# Request Validation Error
@app.exception_handler(RequestValidationError)
async def exception_handler(request, exc: RequestValidationError):
    list(map(lambda i: i.pop('url', None), exc.errors()))
    return JSONResponse(
        status_code=400,
        content={
            "data": [],
            "message": (
                f"Failed Endpoint: {request.url}\n"
                f"Failed Method: {request.method}\n"
                f"Failed Reason: {exc.errors()!r}"
            )
        },
    )


# Add Custom Middleware
class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            request.state.db = SESSION()
            response = await call_next(request)
            return response
        except Exception as e:
            request.state.db.rollback()
            # Get the traceback details
            tb_str = traceback.format_exc()
            logger.error(f"\n<<<---Start of Exception--- \nTraceback:{tb_str}\n ---End of Exception--->")
            return JSONResponse(
                status_code=500,
                content={
                    "data": [],
                    "message": (
                        f"Failed Endpoint: {request.url} \n"
                        f"Failed Method: {request.method} \n"
                        f"Failed Reason: {str(e).strip()!r}"
                    )
                },
            )
        finally:
            request.state.db.close()


app.add_middleware(ExceptionMiddleware)
