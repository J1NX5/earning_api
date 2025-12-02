# from typing import Union
from fastapi import FastAPI

# Is actual not implemented
@app.get("/api/{symbol}")
def read_root(symbol):
    return {"data": data}

@app.get("/watch/{symbol}")
def read_root(symbol):
    return {"data": data}