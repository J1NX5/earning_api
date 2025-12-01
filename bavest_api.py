import requests
import os
from dotenv import load_dotenv

class BavestCollector:

    def __init__(self):
        load_dotenv()
        self.url = "https://api.bavest.co/v0/list/symbols"
        self.payload = { "page": 1 }
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-api-key": os.getenv('BAVEST_KEY')
        }

    def call_symbols(self):
        response = requests.post(self.url, json=self.payload, headers=self.headers)
        print(response.text)
    

if __name__ == '__main__':
    bco = BavestCollector()
    bco.call_symbols()