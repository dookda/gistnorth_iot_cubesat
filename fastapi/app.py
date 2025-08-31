from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os

app = FastAPI()

app.mount("/web", StaticFiles(directory="static"), name="static")


@app.get("/api")
def read_root():
    return {"Hello": "World"}
