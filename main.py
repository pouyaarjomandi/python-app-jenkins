from fastapi import FastAPI
import os

app = FastAPI()

APP_ENV = os.getenv("APP_ENV", "development")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")


@app.get("/")
def root():
    return {
        "message": "Hello from Python!",
        "env": APP_ENV,
        "version": APP_VERSION,
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id, "name": f"Item {item_id}"}
