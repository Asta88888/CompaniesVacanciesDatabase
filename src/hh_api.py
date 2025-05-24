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


def get_vacancies(company_id) -> list[dict[str, Any]]:
    """Подключение к API HeadHunter для получения списка вакансий по заданному ID компании"""
    vacancies = []
    page = 0
    per_page = 100
    while True:
        response = requests.get(
            "https://api.hh.ru/vacancies",
            params={"employer_id": company_id, "per_page": per_page, "page": page}
        )
        if response.status_code != 200:
            raise Exception(f"Ошибка при запросе списка вакансий: {response.status_code}")
        data = response.json()
        vacancies.extend(data.get("items", []))
        if page >= data.get("pages", 0) - 1:
            break
        page += 1
    return vacancies



