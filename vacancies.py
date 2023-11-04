import datetime
from datetime import datetime
import json

path_vacancies_hh = "./vacancies_hh.json"
path_vacancies_sj = "./vacancies_sj.json"

class Vacancy:

    def __init__(self):
        self.all_vacancies_hh = self.load_vacancies_hh()
        self.all_vacancies_sj = self.load_vacancies_sj()


    def load_vacancies_hh(self):
        with open(path_vacancies_hh, encoding='UTF-8') as file:
            all_vacancies_hh = json.load(file)
            return all_vacancies_hh

    def load_vacancies_sj(self):
        with open(path_vacancies_sj, encoding='UTF-8') as file:
            all_vacancies_sj = json.load(file)
            return all_vacancies_sj


    def get_atribute_vacancy_hh(self):
        vacancy_hh = {}
        for i in self.load_vacancies_hh()['items']:
            published_date_hh = datetime.strptime(i.get('published_at'), "%Y-%m-%dT%H:%M:%S%z")
            vacancy_hh['id вакансии'] = i['id']
            vacancy_hh['название вакансии'] = i['name']
            vacancy_hh['заработная плата'] = i.get('salary')
            vacancy_hh['валюта заработной платы'] = i.get('currency')
            vacancy_hh['ссылка на вакансию'] = i['alternate_url']
            vacancy_hh['обязанности'] = i['snippet']['requirement']
            vacancy_hh['дата публикации вакансии'] = published_date_hh.strftime("%d.%m.%Y")
        return vacancy_hh


    def get_atribute_vacancy_sj(self):
        vacancy_sj = {}
        for i in self.load_vacancies_sj()['objects']:
            published_date_sj = datetime.fromtimestamp(i.get('date_published', ''))
            vacancy_sj['id вакансии'] = i['id']
            vacancy_sj['название вакансии'] = i.get('profession', '')
            vacancy_sj['заработная плата'] = i.get('payment_from', '') if i.get('payment_from') else None
            vacancy_sj['валюта заработной платы'] = i.get('currency')
            vacancy_sj['ссылка на вакансию'] = i.get('link')
            vacancy_sj['обязанности'] = i.get('candidat').replace('\n', '') if i.get('candidat') else None
            vacancy_sj['дата публикации вакансии'] = published_date_sj.strftime("%d.%m.%Y")
        return vacancy_sj


v = Vacancy()
print(v.load_vacancies_hh())
print(v.load_vacancies_sj())

