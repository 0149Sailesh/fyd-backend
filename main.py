import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, debug=True)


@app.get("/", tags=["Root"], response_description="Hello World")
async def read_root():
    return {"message": "Hello World"}
