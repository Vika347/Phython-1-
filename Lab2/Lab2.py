def guess_number(target: int, lst: list, method: str = "increment" ) -> list[int | None, int]:
    """Находит число в списке указанным методом и возвращает результат с количеством попыток.

        Arguments:
            target: Искомое число
            lst: Список для поиска
            type: Тип поиска - 'seq' (последовательный), 'bin' (бинарный),
            'bin_with_making_list' (бинарный с составлением списка из двух чисел)

        Returns:
            list: [найденное число или None, количество попыток]
    """
    lst.sort()
    attempts = 0
    if int(target) != target:
        raise TypeError("Таргет - нецелое число")
    if str(target) == target:
        raise TypeError("Таргет - строчное число")
    for x in lst:
        if int(x) != x:
            raise TypeError("В списке есть нецелое число")
        if str(x) == x:
            raise TypeError("В списке есть строчное число")

    if method == "bin_with_making_list":  # бинарный поиск и создание листа из 2х элементов
        if len(lst) == 2:
            lst = list(range(lst[0], lst[1] + 1))
            left, right = 0, len(lst) - 1
            while left <= right:
                attempts += 1
                mid = (left + right) // 2
                if lst[mid] == target:
                    return [target, attempts]  # [таргет, попытки]
                elif lst[mid] < target:
                    left = mid + 1
                else:
                    right = mid - 1
            return [None, attempts]  # число не найдено

    elif method == "bin":  # Бинарный поиск
        left, right = 0, len(lst) - 1
        while left <= right:
            attempts += 1
            mid = (left + right) // 2
            if lst[mid] == target:
                return [target, attempts]  # [таргет, попытки]
            elif lst[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return [None, attempts]  # число не найдено

    elif method == "seq":  # Последовательный поиск
        for i in range(len(lst)):
            attempts += 1
            if lst[i] == target:
                return [target, attempts]  # [таргет, попытки]
        return [None, attempts]  # число не найдено


def main():
    """Функция для ввода пользовательских данных."""
    target = int(input("Введите таргет"))
    type = input("Введите тип поиска - 'seq' (последовательный), 'bin' (бинарный) или 'bin_with_making_list' "
                 "(бинарный поиск с созданием массива из двух чисел)")
    list_your_numb = (input("Введите массив данных через пробел"))
    list_your_numb = [int(i) for i in list_your_numb.split()]
    res = guess_number(target, list_your_numb, type)
    print(res)


if __name__ == "__main__":
    main()
