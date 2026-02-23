from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.core.exceptions import NotFoundException
from src.library.routers import book_router

app = FastAPI()

app.include_router(book_router)


@app.exception_handler(NotFoundException)
async def not_found_handler(request, exc: NotFoundException):
    return JSONResponse(status_code=404, content={"detail": str(exc)})
