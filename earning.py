import os
from dotenv import load_dotenv
import csv
import requests
from db import DBManager
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
        self.dmo = DBManager()

    def get_data_by_symbol(self,symb: str):
        fetch_data = self.dmo.find_by_symbol(symb)
        # logging.info(f'search for data from symbol: {symb}')
        print(f'search for data from symbol: {symb}')
        return fetch_data
        

    def get_earning(self, len_param: int):
        CSV_URL = f'https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon={str(len_param)}month&apikey={self.api_key}'
        with requests.Session() as s:
            download = s.get(CSV_URL)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            for row in my_list:
                if row[0] != 'symbol':
                    # At this point ist row[0] = symbol
                    self.get_earning_estimates(row[0])
                    #print(row[0])
                else:
                    pass

    def get_earning_estimates(self, symb: str):
        url = f'https://www.alphavantage.co/query?function=EARNINGS_ESTIMATES&symbol={symb}&apikey={self.api_key}'
        with requests.Session() as s:
            self.dmo._create_estimate_table()
            # print(s.get(url).json()['estimates'][-1])
            last_est = s.get(url).json()['estimates'][0]
            self.dmo.insert_estimate(symb, last_est['date'], last_est['horizon'], last_est['eps_estimate_average'], last_est['eps_estimate_high'], last_est['eps_estimate_low'],
                    last_est['eps_estimate_analyst_count'], last_est['eps_estimate_average_7_days_ago'],
                    last_est['eps_estimate_average_30_days_ago'], last_est['eps_estimate_average_60_days_ago'],
                    last_est['eps_estimate_average_90_days_ago'], last_est['eps_estimate_revision_up_trailing_7_days'],
                    last_est['eps_estimate_revision_down_trailing_7_days'], last_est['eps_estimate_revision_up_trailing_30_days'],
                    last_est['eps_estimate_revision_down_trailing_30_days'], last_est['revenue_estimate_average'],
                    last_est['revenue_estimate_high'], last_est['revenue_estimate_low'], last_est['revenue_estimate_analyst_count'])




    # def check_news(self, len_param: int):
    #     CSV_URL = f'https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon={str(len_param)}month&apikey={self.api_key}'
    #     with requests.Session() as s:
    #         download = s.get(CSV_URL)
    #         decoded_content = download.content.decode('utf-8')
    #         cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    #         my_list = list(cr)
    #         for row in my_list:
    #              print(row)


if __name__ == '__main__':
    clltr = Collector()
    # clltr.get_earning(3)
    clltr.get_earning_estimates('WLKP')