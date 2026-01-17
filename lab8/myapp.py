from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os

from models.author import Author
from models.app import App
from models.user import User
from models.currency import Currency
from models.user_currency import UserCurrency
from utils.currency_api import get_currencies


class CurrencyHandler(BaseHTTPRequestHandler):
    """Обработчик HTTP запросов"""

    # Путь к шаблонам
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=select_autoescape()
    )

    # Инициализация данных
    author = Author(name="Виктория Родина", group="P3121")
    app = App(name="CurrencyTracker", version="1.0", author=author)

    # Пользователи
    users = [
        User(id=1, name="Алексей Петров"),
        User(id=2, name="Мария Сидорова"),
        User(id=3, name="Иван Иванов")
    ]

    # Валюты
    currencies = [
        Currency(id="R01235", num_code="840", char_code="USD",
                 name="Доллар США", value=92.50, nominal=1),
        Currency(id="R01239", num_code="978", char_code="EUR",
                 name="Евро", value=101.30, nominal=1),
        Currency(id="R01035", num_code="826", char_code="GBP",
                 name="Фунт стерлингов", value=116.80, nominal=1)
    ]

    # Подписки
    user_currencies = [
        UserCurrency(id=1, user_id=1, currency_id="R01235"),
        UserCurrency(id=2, user_id=1, currency_id="R01239"),
        UserCurrency(id=3, user_id=2, currency_id="R01235"),
        UserCurrency(id=4, user_id=3, currency_id="R01035")
    ]

    # Навигация
    navigation = [
        {'caption': 'Главная', 'href': '/'},
        {'caption': 'Пользователи', 'href': '/users'},
        {'caption': 'Валюты', 'href': '/currencies'},
        {'caption': 'Об авторе', 'href': '/author'}
    ]

    def do_GET(self):
        """Обработка GET запросов"""
        parsed = urlparse(self.path)
        path = parsed.path

        if path == '/':
            self.show_index()
        elif path == '/users':
            self.show_users()
        elif path == '/user':
            params = parse_qs(parsed.query)
            self.show_user(params)
        elif path == '/currencies':
            self.show_currencies()
        elif path == '/author':
            self.show_author()
        else:
            self.send_error(404, "Страница не найдена")

    def render_template(self, template_name, **context):
        """Рендеринг шаблона"""
        # Базовые данные
        base_context = {
            'myapp': self.app.name,
            'app_version': self.app.version,
            'author_name': self.author.name,
            'group': self.author.group,
            'navigation': self.navigation
        }

        base_context.update(context)

        template = self.env.get_template(template_name)
        html = template.render(**base_context)

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def show_index(self):
        """Главная страница"""
        self.render_template(
            'index.html',
            users_count=len(self.users),
            currencies_count=len(self.currencies),
            subscriptions_count=len(self.user_currencies)
        )

    def show_users(self):
        """Страница пользователей"""
        users_data = []
        for user in self.users:
            sub_count = len([uc for uc in self.user_currencies if uc.user_id == user.id])
            users_data.append({
                'user': user,
                'subscription_count': sub_count
            })

        self.render_template('users.html', users_data=users_data)

    def show_user(self, params):
        """Страница конкретного пользователя"""
        try:
            user_id = int(params.get('id', [1])[0])
            user = next((u for u in self.users if u.id == user_id), None)

            if not user:
                self.send_error(404, "Пользователь не найден")
                return

            # Получаем ID валют, на которые подписан пользователь
            user_currency_ids = []
            for uc in self.user_currencies:
                if uc.user_id == user.id:
                    user_currency_ids.append(uc.currency_id)

            # Получаем объекты валют
            user_subscriptions = []
            for currency in self.currencies:
                if currency.id in user_currency_ids:
                    user_subscriptions.append(currency)

            # Генерируем email
            email = f"{user.name.lower().replace(' ', '.')}@example.com"

            # Отображаем страницу
            self.render_template(
                'user.html',
                user={
                    'id': user.id,
                    'name': user.name,
                    'email': email
                },
                subscriptions=user_subscriptions,
                subscription_count=len(user_subscriptions)
            )
        except ValueError:
            self.send_error(400, "Некорректный ID пользователя")
        except Exception as e:
            print(f"Ошибка при отображении пользователя: {e}")
            self.send_error(500, "Внутренняя ошибка сервера")

    def show_currencies(self):
        """Страница валют"""
        try:
            # Обновляем курсы из API
            api_rates = get_currencies(['USD', 'EUR', 'GBP'])
            for currency in self.currencies:
                if currency.char_code in api_rates:
                    currency.value = api_rates[currency.char_code]
        except Exception as e:
            print(f"Ошибка API: {e}")

        self.render_template('currencies.html', currencies=self.currencies)

    def show_author(self):
        """Страница об авторе"""
        self.render_template('author.html')


def start_server():
    """Запуск сервера"""
    server = HTTPServer(('localhost', 8000), CurrencyHandler)

    print("Сервер запущен: http://localhost:8000")


    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен")


if __name__ == "__main__":
    start_server()