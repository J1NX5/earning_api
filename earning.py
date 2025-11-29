import os
from dotenv import load_dotenv
import csv
import requests
from db import DBManager
from datetime import datetime, timedelta
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

# AAPLE, LH

class Collector:

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('API_KEY')
        self.api_key_2 = os.getenv('API_KEY_2')
        self.dmo = DBManager()
        self.dmo.create_earning_report_table()
        self.current_date = datetime.today().strftime('%Y-%m-%d')
        self.date_format = "%Y-%m-%d"
        self.current_date_obj = datetime.strptime(self.current_date, self.date_format)
        self.tmp_yesterday = self.current_date_obj - timedelta(days=1)
        self.yesterday_date = str(self.tmp_yesterday.strftime('%Y-%m-%d'))

    def get_data_by_symbol(self,symb: str):
        fetch_data = self.dmo.find_by_symbol(symb)
        # logging.info(f'search for data from symbol: {symb}')
        print(f'search for data from symbol: {symb}')
        return fetch_data

# This function collect much data it os possible
# works
    def get_earning_report(self, symb: str):
        url = f'https://financialmodelingprep.com/stable/earnings?symbol={symb}&apikey={self.api_key_2}'
        with requests.Session() as s:
            data = s.get(url).json()
            print(data)
            for d in range(0,len(data)):
                self.dmo.insert_earning_report( data[d]['symbol'],data[d]['date'],data[d]['epsActual'],data[d]['epsEstimated'],data[d]['revenueActual'], data[d]['revenueEstimated'], data[d]['lastUpdated'], str(self.current_date), 1)

    def get_earning_report_by_range(self, _from: str, _to: str):
            url = f'https://financialmodelingprep.com/stable/earnings-calendar?from={_from}&to={_to}&apikey={self.api_key_2}'
            with requests.Session() as s:
                data = s.get(url).json()
                print(data)
                for d in range(0,len(data)):
                    self.dmo.insert_earning_report( data[d]['symbol'],data[d]['date'],data[d]['epsActual'],data[d]['epsEstimated'],data[d]['revenueActual'], data[d]['revenueEstimated'], data[d]['lastUpdated'], str(self.current_date), 1)



# function for updatin data if null in there


if __name__ == '__main__':
    clltr = Collector()
    # For single run by execute: python earning.py
    # clltr.get_earning()
    
    clltr.get_earning_report_by_range(clltr.yesterday_date, clltr.current_date)

    # it works
    # clltr.get_earning_report('AAPL')