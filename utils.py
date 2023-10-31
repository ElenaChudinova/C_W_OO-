import pprint
from abc import ABC, abstractmethod
import requests
import json
import os
import datetime
import isodate

path_hhru = "./vacancies_hh.json"
path_sjob = "./vacancies_sj.json"


class Vacations(ABC):
    @abstractmethod
    def get_vacancies(self):
        pass


class HHru(Vacations):
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
        response_hh = requests.get(self.url, headers=headers, params=params)
        data = response_hh.json()
        json.dumps(data, skipkeys=False, ensure_ascii=False, default=str, indent=4)
        with open(path_hhru, 'w') as f:
            f.write(data)

        return data



class SuperJob(Vacations):
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
        respons = requests.get(self.url, params=params, headers=headers)
        data = respons.json()
        json.dumps(data, skipkeys=False, ensure_ascii=False, default=str, indent=4)
        with open(path_sjob, 'w') as f:
            f.write(data)

        return data





hh = HHru()
# pprint.pprint(hh.get_vacancies.__dict__)
sj = SuperJob()

# pprint.pprint(sj.get_vacancies.__dict__)
hh.get_vacancies("Python")
sj.get_vacancies("Python")