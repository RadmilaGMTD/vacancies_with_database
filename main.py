from config import config
import psycopg2

from src.interaction_with_API import HeadHunterAPI
from src.interaction_with_database import CreatingDatabaseTables
from src.interaction_with_vacancies import DBManager


def main():
    params = config()
    vacancies_ = HeadHunterAPI()
    result_get_vacancies = vacancies_.get_vacancies("Яндекс")
    result_top_vacancies = vacancies_.top_10_vacancies()
    result_create_database = CreatingDatabaseTables("head_hunter", params)
    res = result_create_database.create_database()
    result_save = result_create_database.save_data_to_database(result_top_vacancies)
    result_manager = DBManager("head_hunter", params)
    result_get_list_companies = result_manager.get_list_companies()
    result_get_list_companies_vacancies = result_manager.get_list_companies_vacancies()
    result_get_avg_salary = result_manager.get_avg_salary()
    result_get_vacancies_with_higher_salary = result_manager.get_vacancies_with_higher_salary()
    result_get_vacancies_with_keyword = result_manager.get_vacancies_with_keyword("Python")

    return result_get_vacancies_with_keyword



if __name__ == '__main__':
    print(main())
