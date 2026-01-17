class Currency():
    def __init__(self, id: str, num_code: str, char_code: str, name: str, value: float, nominal: int):
        self.__id: str = id  # Изменено с int на str
        self.__num_code: str = num_code
        self.__char_code: str = char_code
        self.__name: str = name
        self.__value: float = value
        self.__nominal: int = nominal

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, id: str):
        if isinstance(id, str) and len(id) >= 1:
            self.__id = id
        else:
            raise ValueError('ID должен быть непустой строкой')

    @property
    def num_code(self) -> str:
        return self.__num_code

    @num_code.setter
    def num_code(self, num_code: str):
        if isinstance(num_code, str) and num_code.isdigit():
            self.__num_code = num_code
        else:
            raise ValueError('Код должен состоять из цифр')

    @property
    def char_code(self) -> str:
        return self.__char_code

    @char_code.setter
    def char_code(self, char_code: str):
        if isinstance(char_code, str) and len(char_code) == 3:
            self.__char_code = char_code.upper()
        else:
            raise ValueError('Код должен состоять из 3 символов')

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        if isinstance(name, str) and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError('Название должно быть строкой минимум из 2 символов')

    @property
    def value(self) -> float:
        return self.__value

    @value.setter
    def value(self, value: float):
        if isinstance(value, (int, float)) and value > 0:
            self.__value = float(value)
        else:
            raise ValueError('Курс должен быть положительным числом')

    @property
    def nominal(self) -> int:
        return self.__nominal

    @nominal.setter
    def nominal(self, nominal: int):
        if isinstance(nominal, int) and nominal > 0:
            self.__nominal = nominal
        else:
            raise ValueError('Номинал должен быть положительным целым числом')