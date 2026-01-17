"""
CRUD операции для пользователей и подписок.
Работает с  моделями User и UserCurrency .
"""
from typing import List, Dict, Any
from controllers.database import Database


class UserCRUD:
    """CRUD операции для пользователей и подписок"""

    def __init__(self, db: Database):
        self.db = db

    # === Пользователи ===

    def create_user(self, name: str) -> int:
        """Create: Добавление пользователя"""
        sql = "INSERT INTO users(name) VALUES(?)"
        self.db.execute(sql, (name,))
        self.db.commit()
        return self.db.cursor.lastrowid

    def read_all_users(self) -> List[Dict[str, Any]]:
        """Read: Все пользователи"""
        self.db.execute("SELECT * FROM users ORDER BY id")
        columns = [desc[0] for desc in self.db.cursor.description]
        return [dict(zip(columns, row)) for row in self.db.cursor.fetchall()]

    def read_user_by_id(self, user_id: int) -> Dict[str, Any]:
        """Read: Пользователь по ID"""
        self.db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        columns = [desc[0] for desc in self.db.cursor.description]
        row = self.db.cursor.fetchone()
        return dict(zip(columns, row)) if row else None

    def update_user(self, user_id: int, new_name: str):
        """Update: Обновление имени"""
        sql = "UPDATE users SET name = ? WHERE id = ?"
        self.db.execute(sql, (new_name, user_id))
        self.db.commit()

    def delete_user(self, user_id: int):
        """Delete: Удаление пользователя"""
        # Удаляем подписки
        self.db.execute("DELETE FROM user_currencies WHERE user_id = ?", (user_id,))
        # Удаляем пользователя
        self.db.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.db.commit()

    # === Подписки ===

    def add_subscription(self, user_id: int, currency_id: str) -> int:
        """Добавление подписки"""
        sql = "INSERT INTO user_currencies(user_id, currency_id) VALUES(?, ?)"
        self.db.execute(sql, (user_id, currency_id))
        self.db.commit()
        return self.db.cursor.lastrowid

    def remove_subscription(self, user_id: int, currency_id: str):
        """Удаление подписки"""
        sql = "DELETE FROM user_currencies WHERE user_id = ? AND currency_id = ?"
        self.db.execute(sql, (user_id, currency_id))
        self.db.commit()

    def get_user_subscriptions(self, user_id: int) -> List[Dict[str, Any]]:
        """Получение подписок пользователя"""
        sql = """
            SELECT c.* FROM currencies c
            JOIN user_currencies uc ON c.id = uc.currency_id
            WHERE uc.user_id = ?
            ORDER BY c.char_code
        """
        self.db.execute(sql, (user_id,))
        columns = [desc[0] for desc in self.db.cursor.description]
        return [dict(zip(columns, row)) for row in self.db.cursor.fetchall()]

    def has_subscription(self, user_id: int, currency_id: str) -> bool:
        """Проверка наличия подписки"""
        sql = """
            SELECT COUNT(*) FROM user_currencies 
            WHERE user_id = ? AND currency_id = ?
        """
        self.db.execute(sql, (user_id, currency_id))
        return self.db.cursor.fetchone()[0] > 0

    def count_subscriptions(self, user_id: int) -> int:
        """Количество подписок пользователя"""
        sql = "SELECT COUNT(*) FROM user_currencies WHERE user_id = ?"
        self.db.execute(sql, (user_id,))
        return self.db.cursor.fetchone()[0]

    def count_users(self) -> int:
        """Общее количество пользователей"""
        self.db.execute("SELECT COUNT(*) FROM users")
        return self.db.cursor.fetchone()[0]