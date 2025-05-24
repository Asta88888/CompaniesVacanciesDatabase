import psycopg2
from typing import Any
from src.cleaner import cleaner


def create_database(database_name: str, params: dict) -> None:
    """Создание базы данных для сохранения данных о компаниях и вакансий"""
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    cur.close()
    conn.close()


def create_tables(database_name: str, params: dict) -> None:
    """Создание таблиц 'companies' и 'vacancies' в базе данных
    'companiesvacancies'"""
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS companies (
        company_id SERIAL PRIMARY KEY, 
        name VARCHAR(255) NOT NULL,
        hh_company_id INT UNIQUE,
        open_vacancies INT,
        description TEXT,
        url TEXT
        );
    """)

    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS vacancies (
        vacancy_id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        hh_company_id INT,
        work_format VARCHAR(100),
        salary_min DECIMAL(10, 2),
        salary_max DECIMAL(10, 2),
        description TEXT,
        url TEXT,
        FOREIGN KEY (hh_company_id) REFERENCES companies (hh_company_id) ON DELETE CASCADE
        );
    """)
    conn.commit()
    conn.close()


def save_companies_to_database(data: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """Сохранение информации о компаниях в таблицу 'companies' базы данных
    'companiesvacancies'"""
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        for company in data:
            cur.execute(
                """
                INSERT INTO companies (name, hh_company_id, open_vacancies, description, url)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (hh_company_id) DO NOTHING
                """,
                (
                    company.get("name"),
                    company.get("id"),
                    company.get("open_vacancies"),
                    cleaner(company.get("description", "")),
                    company.get("alternate_url")
                )
            )
        conn.commit()
        conn.close()


def save_vacancies_to_database(vacancies: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """Сохранение информации о вакансиях в таблицу 'vacancies' базы данных
    'companiesvacancies'"""
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        for vacancy in vacancies:
            name = vacancy.get("name")
            hh_company_id = vacancy.get("employer").get("id")
            salary = vacancy.get("salary")
            salary_min = salary["from"] if salary and salary.get("from") is not None else None
            salary_max = salary["to"] if salary and salary.get("to") is not None else None
            work_format = vacancy.get("schedule", {}).get("name")
            snippet = vacancy.get("snippet", {})
            description = snippet.get("requirement") or snippet.get("responsibility") or ""
            url = vacancy.get("alternate_url")

            cur.execute(
            """
            INSERT INTO vacancies (name, hh_company_id, work_format, salary_min, salary_max, description, url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                name,
                hh_company_id,
                work_format,
                salary_min,
                salary_max,
                description,
                url
            )
        )
    conn.commit()
    conn.close()
