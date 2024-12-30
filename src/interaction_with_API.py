from abc import ABC, abstractmethod
from typing import Any

import requests


class Parser(ABC):
    """Абстрактный класс для работы с апи"""

    @abstractmethod
    def _connection_to_api(self) -> Any:
        """Устанавливает соединение с API HeadHunter."""
        pass

    @abstractmethod
    def get_vacancies(self, max_pages: int = 20) -> list:
        """Получает необходимые вакансии по ключевому слову."""
        pass

    @abstractmethod
    def top_10_vacancies(self):
        """Получает 10 вакансий с наибольшим количеством открытых вакансий."""
        pass


class HeadHunterAPI(Parser):
    """Класс для работы с апи"""

    def __init__(self) -> None:
        """Инициализирует класс HeadHunterAPI и задает начальные параметры."""
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 0, 'only_with_vacancies' : True}
        self._vacancies = []

    def _connection_to_api(self) -> Any:
        """Устанавливает соединение с API HeadHunter."""
        response = requests.get(url="https://api.hh.ru/employers", headers=self.__headers, params=self.__params)
        if response.status_code != 200:
            raise ValueError("Не удалось получить вакансии")
        else:
            return response.json()

    def get_vacancies(self, keyword: str = "", max_pages: int = 20) -> list:
        """Получает необходимые вакансии по ключевому слову."""
        self.__params["per_page"] = 100
        if keyword:
            self.__params["text"] = keyword
        while self.__params["page"] != max_pages:
            response = self._connection_to_api()
            self._vacancies += response.get("items", [])
            self.__params["page"] += 1
        return self._vacancies


    def top_10_vacancies(self):
        """Получает 10 вакансий с наибольшим количеством открытых вакансий."""
        sorted_vacancies = sorted(self._vacancies, key=lambda i: i.get("open_vacancies"), reverse=True)
        return sorted_vacancies[:10]
