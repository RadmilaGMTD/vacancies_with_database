from abc import ABC, abstractmethod
from typing import Any

import psycopg2
import requests


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

    def __init__(self, database_name: str, params: dict):
        self.database_name = database_name
        self.params = params

    def create_database(self):
        """Создание базы данных и таблиц для сохранения данных о компаниях и вакансиях."""

        conn = psycopg2.connect(dbname="postgres", **self.params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE IF EXISTS {self.database_name}")
        cur.execute(f"CREATE DATABASE {self.database_name}")

        conn.close()
        cur.close()

        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE companies (
                    companies_id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    companies_url VARCHAR(255),
                    open_vacancies INTEGER
                )
            """
            )

        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE vacancies (
                    vacancies_id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    salary_from INTEGER,
                    salary_to INTEGER,
                    snippet text,
                    schedule VARCHAR(50),
                    experience VARCHAR(255),
                    companies_id INTEGER REFERENCES companies(companies_id),
                    vacancy_url VARCHAR(255)
                )
            """
            )

        conn.commit()
        conn.close()

    def save_data_to_database(self, data: list[dict[str, Any]]):
        """Сохранение данных о компаниях и вакансиях в базу данных."""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            for company in data:
                cur.execute(
                    """INSERT INTO companies(name, companies_url, open_vacancies)
                VALUES (%s, %s, %s)
                RETURNING companies_id""",
                    (company["name"], company["url"], company["open_vacancies"]),
                )
                companies_id = cur.fetchone()[0]
                vacancies_url_2 = company["vacancies_url"]
                response = requests.get(url=vacancies_url_2)
                response_to_json = response.json()
                vacancies = response_to_json.get("items", [])
                for vacancy in vacancies:
                    salary_info = vacancy.get("salary")
                    if not salary_info:
                        salary_from = 0
                        salary_to = 0
                    else:
                        salary_from = vacancy.get("salary", {}).get("from", 0)
                        salary_to = vacancy.get("salary", {}).get("to", 0)
                    cur.execute(
                        """INSERT INTO vacancies(name, salary_from, salary_to, snippet, schedule,
                        experience, vacancy_url, companies_id)
                        VALUES (%s, COALESCE(%s, 0), COALESCE(%s, 0), %s, %s, %s, %s, %s)""",
                        (
                            vacancy.get("name"),
                            salary_from,
                            salary_to,
                            vacancy.get("snippet", {}).get("requirement"),
                            vacancy.get("schedule", {}).get("name"),
                            vacancy.get("experience", {}).get("name"),
                            vacancies_url_2,
                            companies_id,
                        ),
                    )

        conn.commit()
        conn.close()
