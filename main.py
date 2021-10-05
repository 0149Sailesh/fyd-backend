import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import config
from app.db import connect_db
from routes.api import router as api_router

from routes.setu import router as setuRouter

app = FastAPI()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=config.PORT,
        reload=config.RELOAD,
        debug=config.DEBUG,
    )

app.include_router(setuRouter, prefix="/setu")


@app.on_event("startup")
async def startup():
    # db connection
    connect_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, tags=["api"], prefix="/api")


@app.get("/", tags=["Root"], response_description="Hello World")
async def read_root():
    return {"message": "Hello World"}
