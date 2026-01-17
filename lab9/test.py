import sys
import os

# Добавляем текущую директорию (lab9) в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import unittest
from unittest.mock import MagicMock

# Теперь импорты будут работать правильно
from controllers.currency_crud import CurrencyCRUD
from controllers.user_crud import UserCRUD


class TestCurrencyCRUDSimple(unittest.TestCase):
    def test_create_currency_mocked(self):
        """Тестируем создание валюты с моком БД"""
        mock_db = MagicMock()
        crud = CurrencyCRUD(mock_db)
        test_data = {
            'id': 'USD',
            'num_code': '840',
            'char_code': 'USD',
            'name': 'Доллар',
            'value': 75.5,
            'nominal': 1
        }
        crud.create(test_data)
        mock_db.execute.assert_called_once()
        mock_db.commit.assert_called_once()

    def test_read_by_id_mocked(self):
        """Тестируем получение валюты по ID"""
        mock_db = MagicMock()

        # Настраиваем мок курсора
        mock_cursor = MagicMock()
        mock_cursor.description = [('id',), ('name',), ('value',)]
        mock_cursor.fetchone.return_value = ('USD', 'Доллар США', 75.5)
        mock_db.cursor = mock_cursor

        crud = CurrencyCRUD(mock_db)

        # Вызываем метод
        result = crud.read_by_id('USD')

        # Проверяем
        mock_db.execute.assert_called_with(
            "SELECT * FROM currencies WHERE id = ?",
            ('USD',)
        )
        # Проверяем структуру результата
        self.assertEqual(result['id'], 'USD')
        self.assertEqual(result['value'], 75.5)


class TestUserCRUDSimple(unittest.TestCase):
    def test_add_subscription_mocked(self):
        """Тестируем добавление подписки пользователя"""
        mock_db = MagicMock()

        # Настраиваем возвращаемое значение
        mock_cursor = MagicMock()
        mock_cursor.lastrowid = 100  # ID новой подписки
        mock_db.cursor = mock_cursor

        crud = UserCRUD(mock_db)

        # Вызываем метод
        result = crud.add_subscription(user_id=1, currency_id='USD')

        # Проверяем SQL запрос
        expected_sql = "INSERT INTO user_currencies(user_id, currency_id) VALUES(?, ?)"
        expected_params = (1, 'USD')

        mock_db.execute.assert_called_with(expected_sql, expected_params)
        mock_db.commit.assert_called_once()
        self.assertEqual(result, 100)  # Проверяем возвращенный ID

    def test_get_user_subscriptions_mocked(self):
        """Тестируем получение подписок пользователя"""
        mock_db = MagicMock()

        # Настраиваем возвращаемые данные
        mock_cursor = MagicMock()
        mock_cursor.description = [('id',), ('char_code',), ('name',)]
        mock_cursor.fetchall.return_value = [
            ('USD', 'USD', 'Доллар США'),
            ('EUR', 'EUR', 'Евро')
        ]
        mock_db.cursor = mock_cursor

        crud = UserCRUD(mock_db)

        # Вызываем метод
        result = crud.get_user_subscriptions(1)

        # Проверяем
        self.assertEqual(len(result), 2)  # Две подписки
        self.assertEqual(result[0]['char_code'], 'USD')
        self.assertEqual(result[1]['name'], 'Евро')


if __name__ == '__main__':
    unittest.main()