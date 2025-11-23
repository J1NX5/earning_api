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
                if row[0] == 'symbol':
                    pass
                else:
                    self.dmo.insert_data(row[0],row[1],row[2],row[3],row[4],row[5], row[6])
        # logging.info("run get_earning")
        print("run get_earning")
    
    def check_news(self, len_param: int):
        count = 0
        CSV_URL = f'https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon={str(len_param)}month&apikey={self.api_key}'
        with requests.Session() as s:
            download = s.get(CSV_URL)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            for row in my_list:
                if row[0] == 'symbol':
                    pass
                else:
                    o_row = self.dmo.find_by_symbol_name(row[0], row[1])
                    if self._check_diff_reportdate(o_row, row):
                        self.dmo.insert_data(row[0],row[1],row[2],row[3],row[4],row[5], row[6])
                        count += 1
                        logging.info("Found something new data")
            if count == 0:
                # logging.info("Found no new data")
                print("Found no new data")
        # logging.info("run check_news")
        print("run check_news")

    def _check_diff_reportdate(self, row_1, row_2) -> bool:
        # row_1 are the data from the db
        # row_2 are the new data
        state = False
        # if not database there row_1 will be None
        if row_1 is None:
            self.get_earning(3)

        # At this point we want to check if reportDate is different
        # The rows hav different length because the data from the db has id in addition
        if row_1[3] != row_2[2]:
            state = True
        
        return state


if __name__ == '__main__':
    clltr = Collector()
    # clltr.get_earning(3)
    clltr.check_news(3)