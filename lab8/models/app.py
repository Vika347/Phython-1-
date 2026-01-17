from .author import Author

class App:
    def __init__(self, name: str, version: str, author: Author):
        self.__name: str = name
        self.__version: str = version
        self.__author: Author = author

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        if isinstance(name, str) and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError('Название приложения должно быть строкой длиной не менее 2 символов')

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, version: str):
        if isinstance(version, str) and len(version) >= 1:
            self.__version = version
        else:
            raise ValueError('Версия должна быть строкой')

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, author: Author):
        if isinstance(author, Author):
            self.__author = author
        else:
            raise ValueError('Автор должен быть экземпляром класса Author')