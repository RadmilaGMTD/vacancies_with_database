from config import config
import psycopg2

from src.interaction_with_API import HeadHunterAPI
from src.interaction_with_database import CreatingDatabaseTables


# def main():
#     params = config()
#     vacancies_ = HeadHunterAPI()
#     rew = vacancies_.get_vacancies()
#     res_1 = vacancies_.top_10_vacancies()
#     obj = CreatingDatabaseTables("head_hunter", params)
#     res = obj.create_database()
#     result = obj.save_data_to_database(res_1)
#     return result
#
# if __name__ == '__main__':
#     main()




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


if __name__ == '__main__':
    params = config()

    obj_2 = DBManager("head_hunter", params)
    res_2 = obj_2.get_list_companies()
    res_3 = obj_2.get_list_companies_vacancies()
    print(res_3)