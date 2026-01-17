"""
CRUD операции для валют.
Работает с  моделью Currency .
"""
from typing import List, Dict, Any
from controllers.database import Database


class CurrencyCRUD:
    """CRUD операции для таблицы currencies"""

    def __init__(self, db: Database):
        self.db = db

    def create(self, currency_data: Dict[str, Any]) -> str:
        """Create: Добавление новой валюты"""
        sql = """
            INSERT INTO currencies(id, num_code, char_code, name, value, nominal)
            VALUES(?, ?, ?, ?, ?, ?)
        """
        self.db.execute(sql, (
            currency_data['id'],
            currency_data['num_code'],
            currency_data['char_code'],
            currency_data['name'],
            currency_data['value'],
            currency_data['nominal']
        ))
        self.db.commit()
        return currency_data['id']

    def read_all(self) -> List[Dict[str, Any]]:
        """Read: Все валюты"""
        self.db.execute("SELECT * FROM currencies ORDER BY char_code")
        columns = [desc[0] for desc in self.db.cursor.description]
        return [dict(zip(columns, row)) for row in self.db.cursor.fetchall()]

    def read_by_id(self, currency_id: str) -> Dict[str, Any]:
        """Read: Валюта по ID"""
        self.db.execute("SELECT * FROM currencies WHERE id = ?", (currency_id,))
        columns = [desc[0] for desc in self.db.cursor.description]
        row = self.db.cursor.fetchone()
        return dict(zip(columns, row)) if row else None

    def read_by_char_code(self, char_code: str) -> Dict[str, Any]:
        """Read: Валюта по буквенному коду"""
        self.db.execute("SELECT * FROM currencies WHERE char_code = ?", (char_code,))
        columns = [desc[0] for desc in self.db.cursor.description]
        row = self.db.cursor.fetchone()
        return dict(zip(columns, row)) if row else None

    def update_value(self, currency_id: str, new_value: float):
        """Update: Обновление курса"""
        sql = "UPDATE currencies SET value = ? WHERE id = ?"
        self.db.execute(sql, (new_value, currency_id))
        self.db.commit()

    def update_batch(self, updates: Dict[str, float]):
        """Update: Пакетное обновление"""
        for currency_id, value in updates.items():
            sql = "UPDATE currencies SET value = ? WHERE id = ?"
            self.db.execute(sql, (value, currency_id))
        self.db.commit()

    def delete(self, currency_id: str):
        """Delete: Удаление валюты"""
        # Удаляем подписки сначала
        self.db.execute("DELETE FROM user_currencies WHERE currency_id = ?", (currency_id,))
        # Удаляем валюту
        self.db.execute("DELETE FROM currencies WHERE id = ?", (currency_id,))
        self.db.commit()

    def count(self) -> int:
        """Количество валют"""
        self.db.execute("SELECT COUNT(*) FROM currencies")
        return self.db.cursor.fetchone()[0]