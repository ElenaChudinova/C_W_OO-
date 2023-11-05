from abc import ABC, abstractmethod
from configparser import ParsingError
import requests
import json
import os


path_vacancies = "./vacancies.json"
api_key_sj = os.getenv('API-KEY-SuperJob')


class Vacations(ABC):

    @abstractmethod
    def get_request(self):
        pass
    @abstractmethod
    def get_vacancies(self):
        pass


class HHru(Vacations):
    def __init__(self, keyword):
        self.url = 'https://api.hh.ru/vacancies'
        self.params = {
            "per_page": 100,
            "page": None,
            "keyword": keyword,
            "archive": False,
            "currency": "RUR",
        }
        self.headers = {
            "User-Agent": "Vacancies_ParserApp/1.0"
        }

        self.vacancies = []

    def get_request(self):
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения вакансий! Статус: {response.status_code}")
        return response.json()["items"]
    def get_vacancies(self, pages_count=10):
        self.vacancies = []
        for page in range(pages_count):
            page_vacancies = []
            self.params["page"] = page
            try:
                page_vacancies = self.get_request()
            except ParsingError as error:
                print(error)
            else:
                self.vacancies.extend(page_vacancies)
                print(f"Загружено вакансий: {len(page_vacancies)}")
            if len(page_vacancies) == 0:
                break
        return self.vacancies



    def get_formated_vacanies(self):
        formated_vacanies = []
        for vacancy in self.vacancies:
            formated_vacancy = {
                "title": vacancy["name"],
                "id": vacancy["id"],
                "salary_from": vacancy["salary"]["from"],
                "salary_to": vacancy["salary"]["to"],
                "url": vacancy["alternate_url"],
                "requirement": vacancy["snippet"]["requirement"],
                "currency": vacancy["salary"]["currency"],
            }
            if vacancy["salary"]["from"] == "null":
                formated_vacancy["salary_from"] = 0
            elif vacancy["salary"]["to"] == "null":
                formated_vacancy["salary_to"] = 0

            formated_vacanies.append(formated_vacancy)
        return formated_vacanies



class SuperJob(Vacations):

    def __init__(self, keyword):
        self.url = 'https://api.superjob.ru/2.0/vacancies/'
        self.params = {
            "count": 100,
            "page": None,
            "keyword": keyword,
            "archive": False,
            "currency": "rub",
        }
        self.headers = {
            'X-Api-App-Id': api_key_sj
        }
        self.vacancies = []

    def get_request(self):
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения вакансий! Статус: {response.status_code}")
        return response.json()["objects"]

    def get_vacancies(self, pages_count=10):
        self.vacancies = []
        for page in range(pages_count):
            page_vacancies = []
            self.params["page"] = page
            try:
                page_vacancies = self.get_request()
            except ParsingError as error:
                print(error)
            else:
                self.vacancies.extend(page_vacancies)
                print(f"Загружено вакансий: {len(page_vacancies)}")
            if len(page_vacancies) == 0:
                break
        return self.vacancies

    def get_formated_vacanies(self):
        formated_vacanies = []
        for vacancy in self.vacancies:
            formated_vacancy = {
                "title": vacancy["profession"],
                "id": vacancy["id"],
                "salary_from": vacancy["payment_from"],
                "salary_to": vacancy["payment_to"],
                "url": vacancy["alternate_url"],
                "requirement": vacancy["candidat"],
                "currency": vacancy["currency"],
            }
            if vacancy["payment_from"] == "null":
                formated_vacancy["salary_from"] = 0
            elif vacancy["payment_to"] == "null":
                formated_vacancy["salary_to"] = 0

            formated_vacanies.append(formated_vacancy)
        return formated_vacanies


class Vacancy:
    def __init__(self, vacancy):
        self.title = vacancy["title"]
        self.id = vacancy["id"]
        self.salary_from = vacancy["salary_from"]
        self.salary_to = vacancy["salary_to"]
        self.url = vacancy["url"]
        self.requirement = vacancy["requirement"]

    def __str__(self):
        if not self.salary_from and not self.salary_to:
            salary = "Не указана"
        else:
            salary_from, salary_to = "", ""
            salary = " ".join([salary_from, salary_to]).strip()
        return f"""
        ID вакансии: \n"
        Вакансия: \"{self.title}"
        Зарплата: \"{salary}"
        Ссылка: \"{self.url}"
        Опыт: \"{self.requirement}"
        """

    def __lt__(self, other):
        return int(self.salary_from) < int(other.salary_from)

    def __gt__(self, other):
        return int(self.salary_from) > int(other.salary_from)



class Connector:
    def __init__(self, keyword):
        self.path_vacancies = f"{keyword.title()}.json()"

    def insert(self, vacancies_json):
        with open(self.path_vacancies, "w", encoding='UTF-8') as file:
            json.dump(vacancies_json, file, skipkeys=False, ensure_ascii=False, default=str, indent=4)

    def select(self):
        with open(self.path_vacancies, "r", encoding='UTF-8') as file:
            vacancies = json.load(file)
        return [Vacancy(x) for x in vacancies]

    def sort_by_salary_from(self):
        desc = True if input(
            "> - DESC \n"
            "< - ASC \n>>>"
        ).lower() == ">" else False
        vacancies = self.select()
        return sorted(vacancies, key=lambda x: (x.salary_from if x.salary_from else 0, x.salary_to if x.salary_to else 0), reverse=desc)

