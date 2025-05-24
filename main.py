from src.hh_api import get_companies, get_vacancies
from src.database import create_database, create_tables, save_companies_to_database, save_vacancies_to_database
from src.config import config
from src.db_manager import DBManager


def main():
    # company_ids = [1740, 3529, 78638, 15478, 64174, 3127, 4181, 4934, 3388, 80]
    params = config()
    # companies = get_companies(company_ids)
    #
    # create_database("companiesvacancies", params)
    # create_tables("companiesvacancies", params)
    #
    # save_companies_to_database(companies, "companiesvacancies", params)
    # for company_id in company_ids:
    #     vacancies = get_vacancies(company_id)
    #     save_vacancies_to_database(vacancies, "companiesvacancies", params)

    db = DBManager("companiesvacancies", params)
    # companies_with_quality_vacancies = db.get_companies_and_vacancies_count()
    # for company_name, vacancies_count in companies_with_quality_vacancies:
    #         print(f"Компания: {company_name}, Кол-во вакансий: {vacancies_count}")
    #
    # vacancy_info = db.get_all_vacancies()
    # for company_name, vacancy_name, salary_min, salary_max, url in vacancy_info:
    #     print(f"Компания: {company_name}\nВакансия: {vacancy_name}\nЗаработная плата: {salary_min} - {salary_max},\n {url}\n")

    # avg_salary = db.get_avg_salary()
    # print(f"Средняя зарплата по всем вакансиям - {round(avg_salary)}")

    # higher_salary_vacancy = db.get_vacancies_with_higher_salary()
    # for company_name, vacancy_name, salary_min, salary_max, url in higher_salary_vacancy:
    #     print(f"Компания: {company_name}\nВакансия: {vacancy_name}\nЗаработная плата: {salary_min} - {salary_max}\n{url}")

    keyword_finder = db.get_vacancies_with_keyword("python")
    for company_name, vacancy_name, salary_min, salary_max, url in keyword_finder:
        print(f"Компания: {company_name}\nВакансия: {vacancy_name}\nЗаработная плата: {salary_min} - {salary_max}\n{url}")


if __name__ == '__main__':
    main()

