from config import config
from src.interaction_with_API import HeadHunterAPI
from src.interaction_with_database import CreatingDatabaseTables
from src.interaction_with_vacancies import DBManager


def main() -> None:
    """Функция для взаимодействия с пользователем"""
    params = config()
    vacancies_api = HeadHunterAPI()
    search_query = input("Вас интересует определенная компания? Если нет, пропустите: ").lower()
    vacancies_api.get_vacancies(search_query) if search_query else vacancies_api.get_vacancies("")
    result_top_vacancies = vacancies_api.top_10_vacancies()
    result_create_database = CreatingDatabaseTables("head_hunter", params)
    result_create_database.create_database()
    result_create_database.save_data_to_database(result_top_vacancies)
    result_manager = DBManager("head_hunter", params)

    try:
        while True:
            user_input = input(
                "Выберите опцию:\n"
                "1. Получить список всех компаний и количество вакансий.\n"
                "2. Получить список всех вакансий с указанием названия компании, вакансии, зарплаты и ссылки.\n"
                "3. Получить среднюю зарплату по вакансиям.\n"
                "4. Получить вакансии с зарплатой выше средней.\n"
                "5. Получить вакансии с определённым словом в названии.\n"
                "0. Выход\n: "
            )
            if user_input == "1":
                print(result_manager.get_list_companies())
            elif user_input == "2":
                print(result_manager.get_list_companies_vacancies())
            elif user_input == "3":
                print(f"Средняя зарплата по вакансиям: {result_manager.get_avg_salary()}")
            elif user_input == "4":
                print(result_manager.get_vacancies_with_higher_salary())
            elif user_input == "5":
                keyword = input("Введите слово для поиска в названии вакансий: ").lower()
                print(result_manager.get_vacancies_with_keyword(keyword))
            elif user_input == "0":
                print("Выход из программы.")
                break
            else:
                print("Некорректный ввод. Пожалуйста, выберите число от 1 до 5.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        result_manager.close()


if __name__ == "__main__":
    main()
