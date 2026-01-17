class User:
    def __init__(self, id: int, name: str):
        self.__id: int = id
        self.__name: str = name
        self.__subscriptions = []  # список ID валют

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: int):
        if isinstance(id, int) and id > 0:
            self.__id = id
        else:
            raise ValueError('ID должен быть положительным целым числом')

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        if isinstance(name, str) and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError('Имя должно быть строкой длиной не менее 2 символов')

    @property
    def subscriptions(self):
        return self.__subscriptions

    def add_subscription(self, currency_id: str):
        if currency_id not in self.__subscriptions:
            self.__subscriptions.append(currency_id)

    def remove_subscription(self, currency_id: str):
        if currency_id in self.__subscriptions:
            self.__subscriptions.remove(currency_id)

    def has_subscription(self, currency_id: str) -> bool:
        return currency_id in self.__subscriptions