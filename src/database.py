import psycopg2
from typing import Any
from src.cleaner import cleaner


def create_database(database_name: str, params: dict) -> None:
    """Создание базы данных и таблиц для сохранения данных о компаниях и вакансий"""
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    cur.close()
    conn.close()


def create_tables(database_name, params):
    """Создание таблиц в базе данных 'companiesvacancies'"""
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS companies (
        company_id SERIAL PRIMARY KEY, 
        name VARCHAR(255) NOT NULL,
        open_vacancies INT,
        description TEXT,
        url TEXT
        );
    """)

    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS vacancies (
        vacancy_id SERIAL PRIMARY KEY,
        company_id INT REFERENCES companies(company_id),
        name VARCHAR(100) NOT NULL,
        work_format VARCHAR(100),
        salary_min DECIMAL(10, 2),
        salary_max DECIMAL(10, 2),
        description TEXT
        );
    """)
    conn.commit()
    conn.close()


def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """Сохранение информации о компаниях и вакансиях в таблицы базы данных"""
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        for company in data:
            cur.execute(
                """
                INSERT INTO companies (name, open_vacancies, description, url)
                VALUES (%s, %s, %s, %s)
                RETURNING company_id
                """,
                (
                    company.get("name"),
                    company.get("open_vacancies"),
                    cleaner(company.get("description", "")),
                    company.get("alternate_url")
                )
            )
            company_id = cur.fetchone()[0]

            for vacancy in company.get("vacancies_url", []):

                name = vacancy.get("name")
                salary = vacancy.get("salary")
                salary_min = salary["from"] if salary and salary.get("from") is not None else None
                salary_max = salary["to"] if salary and salary.get("to") is not None else None
                work_format = vacancy.get("schedule", {}).get("name")
                snippet = vacancy.get("snippet", {})
                description = snippet.get("requirement") or snippet.get("responsibility") or ""
                vacancy_url = vacancy.get("alternate_url")

            cur.execute(
                    """
                    INSERT INTO vacancies (company_id, name, work_format, salary_min, salary_max, description)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        company_id,
                        name,
                        work_format,
                        salary_min,
                        salary_max,
                        description,
                        vacancy_url
                    )
                )
    conn.commit()
    conn.close()
