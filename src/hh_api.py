from typing import Any
import requests


def get_companies(company_ids: list[int]) -> list[dict[str, Any]]:
    """Подключение к API HeadHunter для получения списка компаний по заданным ID"""
    companies = []
    for company_id in company_ids:
        response = requests.get(f"https://api.hh.ru/employers/{company_id}", params = {"per_page": 100, "page": 0})
        if response.status_code == 404:
            print(f"Компания с ID {company_id} не найдена.")
            continue
        elif response.status_code != 200:
            print(f"Ошибка при запросе компании {company_id}: {response.status_code}")
            continue
        companies.append(response.json())
    return companies


def get_vacancies(company_id) -> dict[str, Any]:
    """Подключение к API HeadHunter для получения списка вакансий по заданному ID компании"""
    response = requests.get(f"https://api.hh.ru/vacancies", params={"employer_id": company_id, "per_page": 100})
    if response.status_code != 200:
        raise Exception(f"Ошибка при запросе списка вакансий: {response.status_code}")
    data = response.json()
    return data


# if __name__ == "__main__":
#     print(get_companies([1740, 3529, 78638, 15478, 64174, 3127, 4181, 4934, 3388, 80]))
#     print(get_vacancies(1740))
