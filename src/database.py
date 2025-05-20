import psycopg2
from typing import Any


def create_database(database_name: str, params: dict) -> None:
    """Создание базы данных и таблиц для сохранения данных о компаниях и вакансий"""
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE companies (
        company_id SERIAL PRIMARY KEY, 
        name VARCHAR(255) NOT NULL,
        open_vacancies INT,
        description TEXT,
        url TEXT)
        """)

    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE vacancies (
        vacancy_id SERIAL PRIMARY KEY,
        company_id INT REFERENCES companies(company_id),
        name VARCHAR(100) NOT NULL,
        work_format VARCHAR(100),
        salary_min DECIMAL(10, 2),
        salary_max DECIMAL(10, 2),
        description TEXT)
        """)
    conn.commit()
    conn.close()


def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """Сохранение информации о компаниях и вакансиях в таблицы базы данных"""
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        for companies in data:
            company_data = companies["items"]
            cur.execute(
                """
                INSERT INTO companies (name, open_vacancies, description, url)
                VALUES (%s, %s, %s, %s)
                RETURNING company_id
                """,
                (
                    company_data["name"],
                    company_data["open_vacancies"],
                    company_data["description"],
                    company_data["alternate_url"]
                )
            )
    conn.commit()
    conn.close()



