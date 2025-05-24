import psycopg2


class DBManager:
    def __init__(self, db_name: str, params: dict):
        self.conn = psycopg2.connect(dbname=db_name, **params)


    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у
        каждой компании."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT c.name, COUNT(v.vacancy_id) AS vacancies_count
                FROM companies c
                LEFT JOIN vacancies v ON c.hh_company_id = v.hh_company_id
                GROUP BY c.name
                ORDER BY vacancies_count DESC;
                """
            )
            return cur.fetchall()


    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия
        компании, названия вакансии и зарплаты и ссылки на вакансию."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT c.name, v.name, v.salary_min, v.salary_max, v.url
                FROM vacancies v
                JOIN companies c ON v.hh_company_id = c.hh_company_id;
                """
            )
            return cur.fetchall()


    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT AVG((salary_min + salary_max)/2) 
                FROM vacancies
                WHERE salary_min IS NOT NULL AND salary_max IS NOT NULL;
                """
            )
            result = cur.fetchone()
            return result[0] if result else None


    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата
        выше средней по всем вакансиям."""
        avg_salary = self.get_avg_salary()
        if avg_salary is None:
            return []
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT c.name, v.name, v.salary_min, v.salary_max, v.url
                FROM vacancies v
                JOIN companies c ON v.hh_company_id = c.hh_company_id
                WHERE ((v.salary_min + v.salary_max)/2) > %s;
                """, (avg_salary,)
            )
            return cur.fetchall()


    def get_vacancies_with_keyword(self, keyword: str):
        """Получает список всех вакансий, в названии которых
        содержатся переданные в метод слова, например python."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT c.name, v.name, v.salary_min, v.salary_max, v.url
                FROM vacancies v
                JOIN companies c ON v.hh_company_id = c.hh_company_id
                WHERE v.name LIKE %s;
                """
            , (f"%{keyword}%",))
            return cur.fetchall()
