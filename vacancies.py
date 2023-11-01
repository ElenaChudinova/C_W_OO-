import os
import time

import requests
import json

path_vacancies = "./vacancies.json"


class Vacancies:

    def __init__(self, text=str):
        self.hhru_url = 'https://api.hh.ru/vacancies'
        self.sj_url = 'https://api.superjob.ru/2.0/vacancies/'

    def to_json_hhru(self):
        response_hh = requests.get(self.hhru_url, params={"text": "Python"}).json()
        with open(path_vacancies, 'w', encoding='UTF-8') as f:
            json.dump(response_hh, f, skipkeys=False, ensure_ascii=False, default=str, indent=4)
            return response_hh


    def to_json_sujob(self):
        response_sj = requests.get(self.sj_url, params={"text": "Python"}).json()
        with open(path_vacancies, 'a', encoding='UTF-8') as f:
            json.dump(response_sj, f, skipkeys=False, ensure_ascii=False, default=str, indent=4)
            return response_sj

    def read_json_file(self):
        with open(path_vacancies, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data




v = Vacancies()
v.to_json_hhru()
v.to_json_sujob()
print(v.read_json_file())
