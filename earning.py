import os
from dotenv import load_dotenv
import csv
import requests
from db import DBManager
from datetime import datetime
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

class Collector:

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('API_KEY')
        self.api_key_2 = os.getenv('API_KEY_2')
        self.dmo = DBManager()
        self.current_date = datetime.today().strftime('%Y-%m-%d')

    def get_data_by_symbol(self,symb: str):
        fetch_data = self.dmo.find_by_symbol(symb)
        # logging.info(f'search for data from symbol: {symb}')
        print(f'search for data from symbol: {symb}')
        return fetch_data
        
# This function call all symbols which are in earning
    def get_earning(self, len_param: int):
        url = f'https://financialmodelingprep.com/stable/earnings-calendar?apikey={self.api_key_2}'
        with requests.Session() as s:
            e_data = s.get(url).json()
            # For each symbol we want to call the report
            for d in range(0,len(e_data)):
                print(self.current_date)
                try:
                    self.get_earning_report(e_data[d]['symbol'])
                except Exception as e:
                    pass
                    print(e)

# This function collect much data it os possible
    def get_earning_report(self, symb: str):
        url = f'https://financialmodelingprep.com/stable/earnings?symbol={symb}&limit=3&apikey={self.api_key_2}'
        with requests.Session() as s:
            self.dmo.create_earning_report_table()
            data = s.get(url).json()
            for d in range(0,len(data)):
                self.dmo.insert_earning_report(data[d]['symbol'],data[d]['date'],data[d]['epsActual'],data[d]['epsEstimated'],data[d]['revenueActual'], data[d]['revenueEstimated'], data[d]['lastUpdated'])




if __name__ == '__main__':
    clltr = Collector()
    # For single run by execute: python earning.py
    clltr.get_earning(3)
    # clltr.get_earning_report('AAPL')