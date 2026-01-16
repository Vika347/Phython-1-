"""
Тесты для лабораторной работы 7.
"""

import unittest
import io


from decorators import logger
from currency_api import get_currencies
from demo_quadratic import solve_quadratic


class TestGetCurrencies(unittest.TestCase):
    """
    Тестирование функции get_currencies.
    """

    def test_valid_currency(self):
        """Проверка возврата существующих валют."""
        result = get_currencies(['USD', 'EUR'])
        self.assertIn("USD", result)
        self.assertIn("EUR", result)
        self.assertIsInstance(result['USD'], float)
        self.assertIsInstance(result['EUR'], float)

    def test_nonexistent_currency(self):
        """Проверка исключения KeyError для несуществующей валюты."""
        with self.assertRaises(KeyError):
            get_currencies(['XYZ'])

    def test_connection_error(self):
        """Проверка ConnectionError при ошибке подключения."""
        with self.assertRaises(ConnectionError):
            get_currencies(['USD'], url="https://invalid-url")

    def test_invalid_json(self):
        """Проверка ValueError при некорректном JSON."""
        with self.assertRaises(ValueError):
            get_currencies(['USD'], url="https://example.com")


class TestLoggerDecorator(unittest.TestCase):
    """
    Тестирование декоратора logger.
    """

    def setUp(self):
        self.stream = io.StringIO()

    def test_logging_success(self):
        """Проверка логирования при успешном выполнении."""

        @logger(handle=self.stream)
        def test_function(x):
            return x * 2

        result = test_function(5)

        self.assertEqual(result, 10)

        logs = self.stream.getvalue()
        self.assertIn("INFO: Start test_function", logs)
        self.assertIn("INFO: Finished test_function", logs)
        self.assertIn("result=10", logs)

    def test_logging_error(self):
        """Проверка логирования при ошибке."""

        @logger(handle=self.stream)
        def test_function():
            raise ValueError("Тестовая ошибка")

        with self.assertRaises(ValueError):
            test_function()

        logs = self.stream.getvalue()
        self.assertIn("ERROR", logs)
        self.assertIn("ValueError", logs)


class TestStreamWrite(unittest.TestCase):
    """
    Тест из задания 6.3.
    """

    def setUp(self):
        self.stream = io.StringIO()

        @logger(handle=self.stream)
        def wrapped():
            return get_currencies(['USD'], url="https://invalid")

        self.wrapped = wrapped

    def test_logging_error(self):
        """Проверка логирования ошибок при недоступном API."""
        with self.assertRaises(ConnectionError):
            self.wrapped()

        logs = self.stream.getvalue()
        self.assertIn("ERROR", logs)
        self.assertIn("ConnectionError", logs)


class TestSolveQuadratic(unittest.TestCase):
    """
    Тестирование функции solve_quadratic.
    """

    def test_two_roots(self):
        """Проверка функции при двух корнях."""
        result = solve_quadratic(1, -3, 2)
        self.assertEqual(result, (2.0, 1.0))

    def test_one_root(self):
        """Проверка функции при одном корне."""
        result = solve_quadratic(1, 2, 1)
        self.assertEqual(result, -1.0)

    def test_no_real_roots(self):
        """Проверка функции при отсутствии действительных корней."""
        result = solve_quadratic(1, 0, 1)
        self.assertIsNone(result)

    def test_invalid_coefficients(self):
        """Проверка исключения при некорректных аргументах."""
        with self.assertRaises(TypeError):
            solve_quadratic("abc", 2, 1)

    def test_linear_equation(self):
        """Проверка линейного уравнения (a = 0)."""
        result = solve_quadratic(0, 2, -4)
        self.assertEqual(result, 2.0)

    def test_degenerate_equation(self):
        """Проверка(a = b = 0)."""
        with self.assertRaises(ValueError) as context:
            solve_quadratic(0, 0, 5)

        self.assertIn("вырождено", str(context.exception))


if __name__ == "__main__":
    unittest.main(verbosity=2)