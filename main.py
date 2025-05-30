from src.hh_api import get_companies, get_vacancies
from src.database import create_database, create_tables, save_companies_to_database, save_vacancies_to_database
from src.config import config
from src.db_manager import DBManager


def main():
    """Главная функция запускающая все процессы, так же содержащая
    пользовательский интерфейс"""
    company_ids = [1740, 3529, 78638, 15478, 64174, 3127, 4181, 4934, 3388, 80]
    params = config()
    companies = get_companies(company_ids)

    create_database("companiesvacancies", params)
    create_tables("companiesvacancies", params)

    save_companies_to_database(companies, "companiesvacancies", params)
    for company_id in company_ids:
        vacancies = get_vacancies(company_id)
        save_vacancies_to_database(vacancies, "companiesvacancies", params)

    db = DBManager("companiesvacancies", params)

    while True:
        print("\nЗдравствуйте! Выберите необходимое:")
        print("1 - Показать компании и количество вакансий")
        print("2 - Показать все вакансии")
        print("3 - Показать среднюю зарплату по всем вакансиям")
        print("4 - Показать вакансии с зарплатой выше средней")
        print("5 - Поиск вакансий по ключевому слову")
        print("0 - Выход")

        user_input = input("Введите номер необходимого: ")

        if user_input == "1":
            companies_with_quantity_vacancies = db.get_companies_and_vacancies_count()
            for company_name, vacancies_count in companies_with_quantity_vacancies:
                print(f"Компания: {company_name}, Кол-во вакансий: {vacancies_count}")
        elif user_input == "2":
            vacancy_info = db.get_all_vacancies()
            for company_name, vacancy_name, salary_min, salary_max, url in vacancy_info:
                print(
                    f"Компания: {company_name}\nВакансия: {vacancy_name}\nЗаработная плата: {salary_min} - {salary_max},\n {url}\n")
        elif user_input == "3":
            avg_salary = db.get_avg_salary()
            print(f"Средняя зарплата по всем вакансиям - {round(avg_salary)}")
        elif user_input == "4":
            higher_salary_vacancy = db.get_vacancies_with_higher_salary()
            for company_name, vacancy_name, salary_min, salary_max, url in higher_salary_vacancy:
                print(
                    f"Компания: {company_name}\nВакансия: {vacancy_name}\nЗаработная плата: {salary_min} - {salary_max}\n{url}")
        elif user_input == "5":
            keyword = input("Введите ключевое слово для поиска: ")
            keyword_finder = db.get_vacancies_with_keyword(keyword)
            for company_name, vacancy_name, salary_min, salary_max, url in keyword_finder:
                print(
                    f"Компания: {company_name}\nВакансия: {vacancy_name}\nЗаработная плата: {salary_min} - {salary_max}\n{url}")
        elif user_input == "0":
            print("Выход...")
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")


if __name__ == '__main__':
    main()
