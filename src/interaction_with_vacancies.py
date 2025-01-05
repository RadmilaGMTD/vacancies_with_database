from config import config
import psycopg2

from src.interaction_with_API import HeadHunterAPI
from src.interaction_with_database import CreatingDatabaseTables

class DBManager:
    def __init__(self, database_name, params):
        self.database_name = database_name
        self.params = params

    def get_list_companies(self):
        """Получение списка всех компаний и количества вакансий у каждой компании"""

        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""SELECT companies.name, COUNT(vacancies.vacancy_url) FROM companies
            LEFT JOIN vacancies USING(vacancies_url)
            GROUP BY companies.name""")
            result = cur.fetchall()

        conn.commit()
        conn.close()
        return result

    def get_list_companies_vacancies(self):
        """Получение списка всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию."""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""SELECT vacancies.name, companies.name, salary_from, salary_to, vacancy_url FROM vacancies
            LEFT JOIN companies using(vacancies_url)""")
            result = cur.fetchall()

        conn.commit()
        conn.close()
        return result

    def get_avg_salary(self):
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""SELECT AVG(salary_from) FROM vacancies""")
            result = cur.fetchall()

        conn.commit()
        conn.close()
        return result

    def get_vacancies_with_higher_salary(self):
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""SELECT *
            FROM vacancies
            WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)""")
            result = cur.fetchall()
        conn.commit()
        conn.close()
        return result

    def get_vacancies_with_keyword(self, keyword):
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(f"""SELECT * FROM vacancies WHERE name LIKE '%{keyword}%'""")
            result = cur.fetchall()
        conn.commit()
        conn.close()
        return result
