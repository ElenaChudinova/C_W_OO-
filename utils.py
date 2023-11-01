import pprint
from abc import ABC, abstractmethod
import requests
import json
import os
import datetime
import isodate

path_vacancies = "./vacancies.json"


class Vacations(ABC):
    pass



class HHru():
    def __init__(self):
            self.url = 'https://api.hh.ru/vacancies'

    def get_vacancies(self, text=str):
        headers = {"User-Agent": "Vacancies_ParserApp/1.0"}
        params = {
            "text": text,
            "area": 1,
            "per_page": 100,
            "page": 0
        }
        response_hh = requests.get(self.url, headers=headers, params=params).json()
        json.dumps(response_hh, skipkeys=False, ensure_ascii=False, default=str, indent=4)
        return response_hh



class SuperJob():
    def __init__(self):
        self.url = 'https://api.superjob.ru/2.0/vacancies/'


    def get_vacancies(self, text=str):
        headers = {
            'X-Api-App-Id': os.environ.get('API-KEY-SuperJob'),
        }
        params = {
            "text": text,
            "area": 1,
            "count": 100,
            "page": 0,
            "salary": "100000",
        }
        respons_sj = requests.get(self.url, params=params, headers=headers).json()
        json.dumps(respons_sj, skipkeys=False, ensure_ascii=False, default=str, indent=4)
        return respons_sj



hh = HHru()
sj = SuperJob()
#pprint.pprint(hh.get_vacancies("Python"))
pprint.pprint(sj.get_vacancies("Python"))

