import unittest
import sys
import os

# Добавляем родительскую директорию в путь
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from models import Author, App, Currency, User, UserCurrency


class TestAuthorModel(unittest.TestCase):
    """Тестирование модели Author."""

    def test_01_author_creation(self):
        """1. Проверка создания автора."""
        author = Author("Вика", "P31211")
        self.assertEqual(author.name, "Вика")
        self.assertEqual(author.group, "P31211")

    def test_02_author_name_validation(self):
        """2. Проверка валидации имени автора."""
        author = Author("Вика", "P31211")
        with self.assertRaises(ValueError):
            author.name = "В"  # Слишком короткое

    def test_03_author_group_validation(self):
        """3. Проверка валидации группы автора."""
        author = Author("Вика", "P31211")
        with self.assertRaises(ValueError):
            author.group = "P123"  # Длина должна быть > 5


class TestAppModel(unittest.TestCase):
    """Тестирование модели App."""

    def test_04_app_creation(self):
        """4. Проверка создания приложения."""
        author = Author("Вика", "P31211")
        app = App("FinanceApp", "1.0", author)
        self.assertEqual(app.name, "FinanceApp")
        self.assertEqual(app.author, author)

    def test_05_app_name_validation(self):
        """5. Проверка валидации имени приложения."""
        author = Author("Вика", "P31211")
        app = App("App", "1.0", author)
        with self.assertRaises(ValueError):
            app.name = "A"  # Минимум 2 символа


class TestCurrencyModel(unittest.TestCase):
    """Тестирование модели Currency."""

    def test_06_currency_creation(self):
        """6. Проверка создания валюты."""
        currency = Currency(
            id="R01235",
            num_code="840",
            char_code="USD",
            name="Доллар",
            value=92.45,
            nominal=1
        )
        self.assertEqual(currency.char_code, "USD")
        self.assertEqual(currency.value, 92.45)

    def test_07_currency_char_code_validation(self):
        """7. Проверка валидации символьного кода."""
        currency = Currency(
            id="R01235",
            num_code="840",
            char_code="USD",
            name="Доллар",
            value=92.45,
            nominal=1
        )
        with self.assertRaises(ValueError):
            currency.char_code = "US"  # Должно быть 3 символа

    def test_08_currency_value_validation(self):
        """8. Проверка валидации значения валюты."""
        currency = Currency(
            id="R01235",
            num_code="840",
            char_code="USD",
            name="Доллар",
            value=92.45,
            nominal=1
        )
        with self.assertRaises(ValueError):
            currency.value = -10  # Должно быть > 0


class TestUserModel(unittest.TestCase):
    """Тестирование модели User."""

    def test_09_user_creation(self):
        """9. Проверка создания пользователя."""
        user = User(101, "Алексей")
        self.assertEqual(user.id, 101)
        self.assertEqual(user.name, "Алексей")
        self.assertEqual(user.subscriptions, [])

    def test_10_user_id_validation(self):
        """10. Проверка валидации ID пользователя."""
        user = User(101, "Алексей")
        with self.assertRaises(ValueError):
            user.id = 0  # Должно быть > 0

    def test_11_user_subscriptions(self):
        """11. Проверка подписок пользователя."""
        user = User(101, "Алексей")
        user.add_subscription("USD")
        user.add_subscription("EUR")
        self.assertEqual(user.subscriptions, ["USD", "EUR"])
        self.assertTrue(user.has_subscription("USD"))

        user.remove_subscription("USD")
        self.assertFalse(user.has_subscription("USD"))


class TestUserCurrencyModel(unittest.TestCase):
    """Тестирование модели UserCurrency."""

    def test_12_user_currency_creation(self):
        """12. Проверка создания связи пользователь-валюта."""
        uc = UserCurrency(1, 101, "USD")  # Проблема: в конструкторе int, в сеттере str
        self.assertEqual(uc.id, 1)
        self.assertEqual(uc.user_id, 101)

    def test_13_user_currency_id_validation(self):
        """13. Проверка валидации ID связи."""
        uc = UserCurrency(1, 101, "USD")
        with self.assertRaises(ValueError):
            uc.id = 0  # Должно быть > 0

    def test_14_user_currency_user_id_validation(self):
        """14. Проверка валидации user_id."""
        uc = UserCurrency(1, 101, "USD")
        with self.assertRaises(ValueError):
            uc.user_id = 0  # Должно быть > 0


class TestIntegration(unittest.TestCase):
    """Интеграционные тесты."""

    def test_15_app_with_author(self):
        """15. Проверка связи приложения и автора."""
        author = Author("Вика", "P31211")
        app = App("CurrencyTracker", "2.0", author)

        self.assertEqual(app.author.name, "Вика")
        self.assertEqual(app.author.group, "P31211")

        # Изменяем автора
        new_author = Author("Анна", "P31212")
        app.author = new_author
        self.assertEqual(app.author.name, "Анна")


if __name__ == '__main__':
    unittest.main()