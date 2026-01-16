#файл-логирование
import logging
from decorators import logger
from currency_api import get_currencies

file_logger = logging.getLogger("currency")
file_logger.setLevel(logging.INFO)
file_logger.addHandler(logging.FileHandler("currency.log", mode="w", encoding="utf-8"))

@logger(handle=file_logger)
def get_currencies_file_logged(*args, **kwargs):
    return get_currencies(*args, **kwargs)


if __name__ == "__main__":
    # Тест : Успешное выполнение
    try:
        print(get_currencies_file_logged(["USD", "EUR"]))
        print("Логи записаны в файл currency.log")
    except Exception as e:
        print("Ошибка:", e)

    # Тест: Несуществующая валюта (для демонстрации ERROR)
    try:
        result = get_currencies_file_logged(["XYZ"])
        print("Результат:", result)
    except Exception as e:
        print("Ожидаемая ошибка:", e)