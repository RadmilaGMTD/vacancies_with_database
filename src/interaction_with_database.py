import psycopg2
from typing import Any
import requests
from abc import ABC, abstractmethod

class BaseDatabase(ABC):
    """Абстрактный класс для создания базы данных и таблиц"""

    @abstractmethod
    def create_database(self):
        """Создание базы данных и таблиц для сохранения данных о компаниях и вакансиях."""
        pass

    @abstractmethod
    def save_data_to_database(self, data: list[dict[str, Any]]):
        """Сохранение данных о компаниях и вакансиях в базу данных."""
        pass


class CreatingDatabaseTables(BaseDatabase):
    """Класс для создания базы данных и таблиц"""

    def __init__(self, database_name, params):
        self.database_name = database_name
        self.params = params

    def create_database(self):
        """Создание базы данных и таблиц для сохранения данных о компаниях и вакансиях."""

        conn = psycopg2.connect(dbname='postgres', **self.params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE {self.database_name}")
        cur.execute(f"CREATE DATABASE {self.database_name}")

        cur.close()

        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE companies (
                    companies_id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    companies_url VARCHAR(255),
                    vacancies_url VARCHAR(255) NOT NULL,
                    open_vacancies INTEGER
                )
            """)

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE vacancies (
                    vacancies_id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    salary_from VARCHAR(50),
                    salary_to VARCHAR(50),
                    snippet text,
                    schedule VARCHAR(50),
                    experience VARCHAR(255),
                    vacancies_url REFERENCES companies(vacancies_url),
                    vacancy_url VARCHAR(255)
                )
            """)

        cur.close()
        conn.close()


    def save_data_to_database(self, data: list[dict[str, Any]]):
        """Сохранение данных о компаниях и вакансиях в базу данных."""

        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            for company in data:
                cur.execute("""INSERT INTO companies(name, companies_url, vacancies_url, open_vacancies)
                VALUES (%s, %s, %s, %s)
                RETURNING companies_id""",
                            (company["name"], company["url"], company["vacancies_url"], company["open_vacancies"]))


                vacancies_url_2 = company["vacancies_url"]
                response = requests.get(url=vacancies_url_2)
                response_to_json = response.json()
                vacancies = response_to_json.get("items", [])
                for vacancy in vacancies:
                    cur.execute("""INSERT INTO vacancies(name, salary_from, salary_to, snippet, schedule, experience, vacancies_url, vacancy_url)
                                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                                (vacancy.get("name"),
                                 vacancy.get("salary", {}).get("from"),
                                 vacancy.get("salary", {}).get("to"),
                                 vacancy.get("snippet", {}).get("requirement"),
                                 vacancy.get("schedule", {}).get("name"),
                                 vacancy.get("experience", {}).get("name"),
                                 vacancies_url_2,
                                 vacancy.get("url")))


        conn.commit()
        conn.close()
