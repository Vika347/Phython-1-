import sys
import logging
from decorators import logger

demo_logger = logging.getLogger("quadratic_demo")
demo_logger.setLevel(logging.INFO)
demo_logger.addHandler(logging.StreamHandler(sys.stdout))


@logger(handle=demo_logger)
def solve_quadratic(a, b, c):
    """
    Решение квадратного уравнения
    Args:
        a: коэффициент при x^2
        b: коэффициент при x
        c: свободный член
    Returns:
        Корни уравнения или сообщение об отсутствии действительных корней
    Raises:
        ValueError: при некорректных коэффициентах
    """
    if not all(isinstance(x, (int, float)) for x in (a, b, c)):
        raise TypeError("Все коэффициенты должны быть числами")

    if a == 0 and b == 0:
        raise ValueError("Уравнение вырождено")

    if a == 0:
        return -c / b

    discriminant = b ** 2 - 4 * a * c

    if discriminant < 0:
        return None  # Нет действительных корней

    if discriminant == 0:
        return -b / (2 * a)

    x1 = (-b + discriminant ** 0.5) / (2 * a)
    x2 = (-b - discriminant ** 0.5) / (2 * a)
    return x1, x2


if __name__ == "__main__":
    ''' 1. Два корня (INFO)'''
    result = solve_quadratic(1, -5, 6)
    print(result)

    ''' 2. Нет корней (WARNING)'''
    result = solve_quadratic(1, 0, 1)
    print(result)

    ''' 3. Ошибка типа (ERROR)'''
    try:
        result = solve_quadratic("abc", 2, 3)
        print(result)
    except Exception as e:
        print(e)

    '''4. Вырожденное уравнение (CRITICAL)'''
    try:
        result = solve_quadratic(0, 0, 5)
        print(result)
    except Exception as e:
        print(e)