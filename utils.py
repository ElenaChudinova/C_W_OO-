from abc import ABC, abstractmethod
import requests
import json
import os


path_vacancies_hh = "./vacancies_hh.json"
path_vacancies_sj = "./vacancies_sj.json"


class Vacations(ABC):
    @abstractmethod
    def get_vacancies(self):
        pass


class HHru(Vacations):
    def __init__(self):
            self.url = 'https://api.hh.ru/vacancies'

    def get_vacancies(self):
        return requests.get(self.url, headers={"User-Agent": "Vacancies_ParserApp/1.0"}, params={'text': 'python', 'page': 0, 'count': 100}).json()

    def to_json_hhru(self):
        response_hh = self.get_vacancies()
        json_object_hh = json.dumps(response_hh, skipkeys=False, ensure_ascii=False, default=str, indent=4)
        with open(path_vacancies_hh, 'w', encoding='UTF-8') as f:
            f.write(json_object_hh)
            return json_object_hh



class SuperJob(Vacations):

    def __init__(self):
        self.url = 'https://api.superjob.ru/2.0/vacancies/'
        self.api_key_sj = os.environ.get('API-KEY-SuperJob')


    def get_vacancies(self):
        return requests.get(self.url, headers={'X-Api-App-Id': self.api_key_sj}, params={'text': 'python', 'page': 0, 'count': 100}).json()

    def to_json_sujob(self):
        response_sj = self.get_vacancies()
        json_object_sj = json.dumps(response_sj, skipkeys=False, ensure_ascii=False, default=str, indent=4)
        with open(path_vacancies_sj, 'w', encoding='UTF-8') as f:
            f.write(json_object_sj)
            return json_object_sj

