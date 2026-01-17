"""
Управление подключением к SQLite БД.
"""
import sqlite3
from typing import Optional


class Database:
    """Класс для управления подключением к БД"""

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None

    def connect(self):
        """Подключение к БД"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        return self

    def disconnect(self):
        """Отключение от БД"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def execute(self, sql: str, params: tuple = ()):
        """Выполнение SQL запроса"""
        if not self.cursor:
            self.connect()
        return self.cursor.execute(sql, params)

    def commit(self):
        """Сохранение изменений"""
        if self.conn:
            self.conn.commit()

    def rollback(self):
        """Откат изменений"""
        if self.conn:
            self.conn.rollback()

    def __enter__(self):
        """Контекстный менеджер"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Выход из контекста"""
        if exc_type:
            self.rollback()
        else:
            self.commit()
        self.disconnect()

    def setup_database(self):
        """Создание таблиц"""
        with self:
            # Таблица пользователей
            self.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
            """)

            # Таблица валют
            self.execute("""
                CREATE TABLE IF NOT EXISTS currencies (
                    id TEXT PRIMARY KEY,
                    num_code TEXT NOT NULL,
                    char_code TEXT NOT NULL,
                    name TEXT NOT NULL,
                    value REAL NOT NULL,
                    nominal INTEGER NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Таблица подписок
            self.execute("""
                CREATE TABLE IF NOT EXISTS user_currencies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    currency_id TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(currency_id) REFERENCES currencies(id)
                )
            """)

            self.commit()