import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import config
from routes.api import router as api_router
from app.db import connect_db

app = FastAPI()

engine = connect_db()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=config.PORT,
        reload=config.RELOAD,
        debug=config.DEBUG,
    )

app.include_router(api_router, tags=["api"], prefix="/api")


@app.get("/", tags=["Root"], response_description="Hello World")
async def read_root():
    return {"message": "Hello World"}
