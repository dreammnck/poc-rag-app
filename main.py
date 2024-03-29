from fastapi import FastAPI
from .routers import ingest, predict
from .utils import log

app = FastAPI()

app.include_router(predict.router)
app.include_router(ingest.router)

@app.get("/")
def root():
    log.logger.info({"root": "OK"})
    return "OK"