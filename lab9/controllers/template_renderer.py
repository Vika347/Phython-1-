"""
Рендеринг Jinja2 шаблонов.
"""
from jinja2 import Environment, FileSystemLoader
import os


class TemplateRenderer:
    """Класс для рендеринга HTML шаблонов"""

    def __init__(self, template_dir: str = "templates"):
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=True
        )

    def render(self, template_name: str, **context) -> str:
        """
        Рендеринг шаблона с контекстом.

        Args:
            template_name: Имя файла шаблона (например, 'index.html')
            **context: Данные для передачи в шаблон

        Returns:
            Готовый HTML
        """
        template = self.env.get_template(template_name)
        return template.render(**context)

    def render_with_base_context(self, template_name: str, app_data: dict, **extra_context) -> str:
        """
        Рендеринг с базовым контекстом (приложение, автор, навигация).

        Args:
            template_name: Имя шаблона
            app_data: Данные приложения {name, version, author_name, group}
            **extra_context: Дополнительные данные

        Returns:
            Готовый HTML
        """
        base_context = {
            'myapp': app_data.get('name', 'Currency App'),
            'app_version': app_data.get('version', '1.0'),
            'author_name': app_data.get('author_name', 'Автор'),
            'group': app_data.get('group', 'Группа'),
            'navigation': [
                {'href': '/', 'caption': 'Главная'},
                {'href': '/users', 'caption': 'Пользователи'},
                {'href': '/currencies', 'caption': 'Валюты'},
                {'href': '/author', 'caption': 'Об авторе'}
            ]
        }

        # Объединяем контексты
        context = {**base_context, **extra_context}
        return self.render(template_name, **context)