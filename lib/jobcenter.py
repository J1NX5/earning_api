from apscheduler.schedulers.background import BackgroundScheduler
import subprocess

class Jobcenter:

    def __init__(self):
        # Define scheduler
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self._get_earning_report_from_fmp, 'interval', minutes=1)

    # Define func for adding by schedular
    def _get_earning_report_from_fmp(self):
        subprocess.run(["python3", "financialmodelingprep.py"])
        print("get_earning_report_from_fmp is running")

    def start(self):
        return self.scheduler.start()
