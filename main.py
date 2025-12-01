# from typing import Union
from fastapi import FastAPI
from lib.api import Api
from lib.watch import Watch
from lib.jobcenter import Jobcenter

app = FastAPI()
jc = Jobcenter()
jc.start()

# Is actual not implemented
@app.get("/api/{symbol}")
def read_root(symbol):
    _api = Api()
    return {"data": data}

@app.get("/watch/{symbol}")
def read_root(symbol):
    _watch = Watch()
    return {"data": data}