from typing import List, Tuple

import psycopg2


class DBManager:
    """Класс для работы с БД"""

    def __init__(self, database_name: str, params: dict):
        self.database_name = database_name
        self.params = params
        self.conn = psycopg2.connect(dbname=self.database_name, **self.params)

    def close(self):
        """Закрывает соединение с базой данных."""
        if self.conn:
            self.conn.close()

    def get_list_companies(self) -> List[Tuple]:
        """Получение списка всех компаний и количества вакансий у каждой компании."""
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT companies.name, COUNT(vacancies.vacancy_url) FROM companies
            LEFT JOIN vacancies ON companies.companies_id=vacancies.companies_id
            GROUP BY companies.name"""
            )
            result = cur.fetchall()
        return result

    def get_list_companies_vacancies(self) -> List[Tuple]:
        """Получение списка всех вакансий с указанием названия компании, вакансии, зарплаты и ссылки."""
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT vacancies.name, companies.name, salary_from, salary_to, vacancy_url FROM vacancies
            LEFT JOIN companies ON vacancies.companies_id=companies.companies_id"""
            )
            result = cur.fetchall()

        return result

    def get_avg_salary(self) -> List[Tuple]:
        """Получает среднюю зарплату по вакансиям."""
        with self.conn.cursor() as cur:
            cur.execute("""SELECT AVG(salary_from) FROM vacancies""")
            result = cur.fetchall()
        return result

    def get_vacancies_with_higher_salary(self) -> List[Tuple]:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT *
            FROM vacancies
            WHERE salary_from > (SELECT avg(salary_from) FROM vacancies WHERE salary_from != 0)"""
            )
            result = cur.fetchall()
        return result

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple]:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        with self.conn.cursor() as cur:
            cur.execute(f"""SELECT * FROM vacancies WHERE name LIKE '%{keyword}%'""")
            result = cur.fetchall()
        return result
