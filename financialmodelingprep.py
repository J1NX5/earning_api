import os
from dotenv import load_dotenv
import csv
import requests
from db import DBManager
from datetime import datetime, timedelta

'''
This is the Collector for financialmodelingprep api.
The api is restricted in free version. 250 Calls per day and not all symbols

The collector only get the current earning reports and controll the data if not complete
'''


class FMP_Collector:

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('FMP_API_KEY')
        self.dmo = DBManager()
        
        # creating table if not exist here
        self.date_format = "%Y-%m-%d"
        self.date_today = datetime.today().strftime('%Y-%m-%d')
        self.date_yesterday = self._get_date_delta_by_days(1)

    def _get_date_delta_by_days(self,day_delay: int) -> str:
        current_date_obj = datetime.strptime(self.date_today, self.date_format)
        tmp_yesterday = self.current_date_obj - timedelta(days=day_delay)
        return str(self.tmp_yesterday.strftime('%Y-%m-%d'))

    
    # A func which get all the earning reports by delay of 1 day
    # The func will called every day by apscheduler in main.py
    def _get_earning_reports_from_to():
        pass


    # A func which is similar to the main concept to handle cases
    # In the func is all what is to do every day
    def job():
        self._get_earning_reports_from_to()
        pass

    # A func which search and insert all historical data from symbols in table


if __name__ == '__main__':
    fmpColl = FMP_Collector()
    fmpColl.job()