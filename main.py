from src.hh_api import get_companies, get_vacancies
from src.database import create_database, save_data_to_database
from src.config import config


def main():
    # company_ids = [1740, 3529, 78638, 15478, 64174, 3127, 4181, 4934, 3388, 80]
    # print(get_companies(company_ids))
    # print(get_vacancies(80))

    params = config()
    print(params)
    #
    # data = get_companies(company_ids)
    create_database("CompaniesVacancies", params)
    # save_data_to_database(data, "CompaniesVacancies", params)


if __name__ == '__main__':
    main()

