from datetime import datetime
from abc import ABC, abstractmethod
from configparser import ParsingError
import requests
import json
import os

path_vacancies = "./vacancies.json"

# API по ключу
api_key_sj = os.getenv('API-KEY-SuperJob')


class Vacations(ABC):
    # Создаем абстрактный класс для работы с API
    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class HHru(Vacations):
    """
    Создаем класс, наследующийся от абстрактного класса.
    Класс умеет подключаться к API HeadHunter
    и получать вакансии.
    """
    def __init__(self, keyword):
        self.url = 'https://api.hh.ru/vacancies'
        self.params = {
            "area": 113,
            "per_page": 50,
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

    def get_vacancies(self, pages_count):
        # Получаем загруженные страницы с сайта HeadHunter по вакансиям
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
        # Получаем отформатированные вакансии под единый формат
        formated_vacanies = []
        for vacancy in self.vacancies:
            published_date_hh = datetime.strptime(vacancy.get('published_at'), "%Y-%m-%dT%H:%M:%S%z")
            vacancy_title = vacancy.get('name')
            vacancy_area = vacancy.get('area')['name']
            vacancy_url = f"https://hh.ru/vacancy/{vacancy.get('id')}"
            salary = vacancy.get('salary')
            if not salary:
                salary_from = 0
                salary_to = 0
                currency = ''
            else:
                salary_from = salary.get('from')
                salary_to = salary.get('to')
                if not salary_from:
                    salary_from = salary_to
                if not salary_to:
                    salary_to = salary_from
                currency = vacancy.get('salary')['currency']
            experience = vacancy.get('experience')['name']
            requirements = (vacancy.get('snippet')['requirement'])
            vacancy_id = vacancy.get('id')
            vacancy_date = published_date_hh.strftime("%d.%m.%Y")
            if requirements:
                requirements = requirements.strip().replace('<highlighttext>', '').replace('</highlighttext>', '')

            vacancy_info = {
                'title': vacancy_title,
                'id': vacancy_id,
                'area': vacancy_area,
                'url': vacancy_url,
                'salary_from': salary_from,
                'salary_to': salary_to,
                'currency': currency,
                'experience': experience,
                'requirements': requirements,
                'date': vacancy_date,
            }

            formated_vacanies.append(vacancy_info)

        return formated_vacanies


class SuperJob(Vacations):
    """
       Создаем класс, наследующийся от абстрактного класса.
       Класс умеет подключаться к API SuperJob
       и получать вакансии.
       """

    def __init__(self, keyword):
        self.url = 'https://api.superjob.ru/2.0/vacancies/'
        self.params = {
            "count": 50,
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

    def get_vacancies(self, pages_count):
        # Получаем загруженные страницы с сайта SuperJob по вакансиям
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
        # Получаем отформатированные вакансии под единый формат
        formated_vacanies = []
        for vacancy in self.vacancies:
            published_date_sj = datetime.fromtimestamp(vacancy.get('date_published', ''))
            formated_vacancy = {
                "title": vacancy.get("profession", ''),
                "id": vacancy["id"],
                "salary_from": vacancy.get("payment_from", '') if vacancy.get("payment_from") else 0,
                "salary_to": vacancy.get("payment_to", '') if vacancy.get("payment_to") else 0,
                "url": vacancy.get("link", 'Default Description') if vacancy.get("link") else None,
                "requirements": vacancy["candidat"].replace('\n', '') if vacancy["candidat"] else None,
                "currency": vacancy["currency"],
                "area": vacancy.get("town")["title"],
                "date": published_date_sj.strftime("%d.%m.%Y"),
            }
            formated_vacanies.append(formated_vacancy)
        return formated_vacanies


class Vacancy:
    """
    Создаем класс для работы с вакансиями. В этом классе определяем нужные нам атрибуты:

    - название вакансии;
    - ссылка на вакансию;
    - зарплата;
    - опыт и требования;
    - город;
    - дата публикации.
    Класс поддерживает методы сравнения вакансий между собой по зарплате.
    """
    def __init__(self, vacancy):
        self.title = vacancy["title"]
        self.id = vacancy["id"]
        self.salary_from = vacancy["salary_from"]
        self.salary_to = vacancy["salary_to"]
        self.url = vacancy["url"]
        self.requirements = vacancy["requirements"]
        self.area = vacancy["area"]
        self.date = vacancy["date"]
        self.currency = vacancy["currency"]

    def __str__(self):
        return f"""
        ID вакансии: \"{self.id}"
        Вакансия: \"{self.title}"
        Зарплата: \"от {self.salary_from} до {self.salary_to} {self.currency}"
        Ссылка: \"{self.url}"
        Опыт и обязанности: \"{self.requirements}"
        Город: \"{self.area}"
        Дата публикации: \"{self.date}"
        """

    def __gt__(self, other):
        return self.salary_from > other.salary_from

    def __lt__(self, other):
        if other.salary_from is None:
            # e.g., 10 < None
            return False
        if self.salary_from is None:
            # e.g., None < 10
            return True

        return self.salary_from < other.salary_from

    def average_salary(self):
        # Функция определяет среднюю зарплату по вакансии
        if self.salary_from and self.salary_to:
            return (self.salary_from + self.salary_to) / 2
        elif self.salary_from:
            return self.salary_from
        elif self.salary_to:
            return self.salary_to
        else:
            return 0


class Connector:
    """
    Создаем класс для сохранения информации о вакансиях в JSON-файл, а также получения
    данных из файла по указанным критериям информации о вакансиях
    """
    def __init__(self, keyword):
        self.path_vacancies = f"{keyword.title()}.json()"

    def insert(self, vacancies_json):
        with open(self.path_vacancies, "w", encoding='UTF-8') as file:
            json.dump(vacancies_json, file, skipkeys=False, ensure_ascii=False, default=str, indent=4)

    def select(self):
        with open(self.path_vacancies, "r", encoding='UTF-8') as file:
            vacancies = json.load(file)
            vacancies_list = [Vacancy(x) for x in vacancies]
        return vacancies_list

    def sort_by_salary_from(self):
        # Функция производит сортировку вакансий по минимальной зарплате
        vacancies = self.select()
        sort_vacancies = sorted(vacancies, key=lambda x: x.average_salary())
        return sort_vacancies

    def top_salary(self):
        """
        Функция производит обратную сортировку вакансий по зарплате и выводит ТОП-5
        по самой высокой заработной плате
        """
        vacancies = self.select()
        sort_vacancies = sorted(vacancies, key=lambda x: x.average_salary(), reverse=True)
        return sort_vacancies[:5]
