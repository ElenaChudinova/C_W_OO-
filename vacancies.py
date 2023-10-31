from utils import HHru, SuperJob
import os
import pprint
import time

import requests
import json

path_hhru = "./vacancies_hh.json"
path_sjob = "./vacancies_sj.json"

class Vacancies:

    def __init__(self, text):
        self.hhru = HHru.get_vacancies(text)
        self.sjob = SuperJob.get_vacancies(text)
        # self.hhru_url = 'https://api.hh.ru/vacancies'
        # self.sj_url = 'https://api.superjob.ru/2.0/vacancies/'

    def to_json_hhru(self):
        with open(path_hhru, 'w') as f:
            json.dump(self.hhru, f, skipkeys=False, ensure_ascii=False, default=str, indent=4)
        with open(path_hhru, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data


        # response_hh = requests.get(self.hhru_url, params={"text": "Python"})
        # with open(path_hhru, 'w') as f:
        #     json.dump(response_hh, f, skipkeys=False, ensure_ascii=False, default=str, indent=4)
        # with open(path_hhru, 'r', encoding='utf-8') as file:
        #     data = json.load(file)
        #     return data

    def to_json_sujob(self):
        pass


        # response_sj = requests.get(self.sj_url, headers={'X-Api-App-Id': os.environ.get('API-KEY-SuperJob')}, params={"text": "Python"})
        # with open(path_sjob, 'w') as f:
        #     json.dump(response_sj, f, skipkeys=False, ensure_ascii=False, default=str, indent=4)
        # with open(path_sjob, 'r', encoding='utf-8') as file:
        #     data = json.load(file)
        #     return data



v = Vacancies("Python")
# print(v.to_json_sujob())
print(v.to_json_hhru())




