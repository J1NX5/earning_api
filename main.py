# from typing import Union
from fastapi import FastAPI
from earning import Collector
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
# import logging

# logging.basicConfig(
#     filename="app.log",
#     encoding="utf-8",
#     filemode="a",
#     format="{asctime} - {levelname} - {message}",
#     style="{",
#     datefmt="%Y-%m-%d %H:%M",
#     level=logging.INFO,
# )

app = FastAPI()

# This is a function to run the earning script and will call by scheduler
def earning_task():
    print("Start run earning.py")
    subprocess.run(["python3", "earning.py"])
    print("earning.py processed successfully.")

scheduler = BackgroundScheduler()
# for testing set hours to minutes
scheduler.add_job(earning_task, 'interval', minutes=1)
scheduler.start()

@app.get("/api/{symbol}")
def read_root(symbol):
    clltr = Collector()
    data = clltr.get_data_by_symbol(symbol)
    return {"data": data}