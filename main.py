from utils import HHru, SuperJob, Connector

def main():
    vacancies_json = []
    keyword = input("Введите вакансию для поиска: ").lower()

    hh = HHru(keyword)
    sj = SuperJob(keyword)
    for api in (hh, sj):
        api.get_vacancies(pages_count=1)
        vacancies_json.extend(api.get_formated_vacanies())

    connector = Connector(keyword=keyword)
    connector.insert(vacancies_json)


    while True:
        comand = input(
            "1 - Вывести список вакансий;\n"
            "2 - Отсортировать по минимальной зарплате;\n"
            "3 - Вывести ТОП-5 вакансий по зарплате;\n"
            "0 - для выхода.\n"
            ">>>"
        )
        if comand.lower() == '0':
            break
        elif comand == "1":
            vacancies = connector.select()
        elif comand == "2":
            vacancies = connector.sort_by_salary_from()
        elif comand == "3":
            vacancies = connector.top_salary()


        for vacancy in vacancies:
            print(vacancy, end='\n')


if __name__ == "__main__":
    main()
