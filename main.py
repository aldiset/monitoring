from uvicorn import run
from fastapi import FastAPI
from app.api import router

app = FastAPI()

app.include_router(router=router, tags=["Monitoring"], prefix="")

if __name__=='__main__':
    run(app=app)