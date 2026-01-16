"""
Модуль для работы с API курсов валют ЦБ РФ.
"""

import json
import requests
from typing import Dict, List


def get_currencies(
        currency_codes: List[str],
        url: str = "https://www.cbr-xml-daily.ru/daily_json.js",
        timeout: float = 10.0
) -> Dict[str, float]:
    """
    Получает текущие курсы валют от API Центробанка России.
    Args:
        currency_codes: Список кодов валют (например, ['USD', 'EUR'])
        url: URL API (по умолчанию официальный API ЦБ РФ)
        timeout: Максимальное время ожидания ответа в секундах
    Returns:
        Словарь с курсами валют вида {'USD': 93.25, 'EUR': 101.70}
    Raises:
        ConnectionError: Если API недоступен или произошла сетевая ошибка
        ValueError: Если получен некорректный JSON
        KeyError: Если отсутствует ключ "Valute" или валюта не найдена
        TypeError: Если курс валюты имеет неправильный тип данных
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()  # Проверяем HTTP ошибки

    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Ошибка подключения к API: {e}")

    try:
        data = response.json()
    except json.JSONDecodeError as e:
        raise ValueError(f"Некорректный JSON ответ: {e}")

    # Проверяем наличие ключа "Valute" в ответе
    if "Valute" not in data:
        raise KeyError("В ответе API отсутствует ключ 'Valute'")

    valutes = data["Valute"]
    result = {}

    # Получаем курсы для каждой запрошенной валюты
    for code in currency_codes:
        code_upper = code.upper()

        if code_upper not in valutes:
            raise KeyError(f"Валюта '{code}' не найдена в данных API")

        currency_info = valutes[code_upper]

        # Проверяем наличие поля "Value"
        if "Value" not in currency_info:
            raise KeyError(f"Для валюты '{code}' отсутствует курс")

        value = currency_info["Value"]

        # Проверяем, что курс - это число
        if not isinstance(value, (int, float)):
            try:
                # Пытаемся преобразовать строку в число
                value = float(str(value).replace(',', '.'))
            except (ValueError, TypeError):
                raise TypeError(f"Некорректный тип курса для '{code}': {type(value)}")

        # Округляем до 2 знаков после запятой
        result[code] = round(float(value), 2)

    return result


# Пример использования (для тестирования)
if __name__ == "__main__":
    # Простой тест функции
    try:
        # Получаем курс доллара
        rates = get_currencies(['USD'])
        print(f"Курс USD: {rates['USD']}")

        # Получаем несколько валют
        rates = get_currencies(['USD', 'EUR', 'GBP'])
        print(f"Курсы валют: {rates}")

    except Exception as e:
        print(f"Произошла ошибка: {type(e).__name__}: {e}")