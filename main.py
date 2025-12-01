# from typing import Union
from fastapi import FastAPI
from earning import Collector
from api import Api
from watch import watch
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess


app = FastAPI()

# Define func for adding by schedular
def get_earning_report_fmp():
    subprocess.run(["python3", "financialmodelingprep.py"])

# Define scheduler
scheduler = BackgroundScheduler()

# Add func and how often it should run
scheduler.add_job(get_earning_report_fmp, 'interval', hours=1)
scheduler.start()



@app.get("/api/{symbol}")
def read_root(symbol):
    _api = Api()
    return {"data": data}

@app.get("/watch/{symbol}")
def read_root(symbol):
    _watch = Watch()
    return {"data": data}