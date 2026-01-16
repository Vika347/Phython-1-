import sys
import functools
import logging


def logger(func=None, *, handle=sys.stdout):
    """
    Универсальный декоратор для отслеживания выполнения функций.
    Args:
        func: Функция для обертывания (если None - возвращает декоратор)
        handle: Объект для вывода (консоль, буфер или логгер)
    Returns:
        Функцию с добавленным логированием
    """

    if func is None:
        return lambda real_func: logger(real_func, handle=handle)

    @functools.wraps(func)
    def inner(*args, **kwargs):
        kwargs.pop('handle', None)
        is_logger = isinstance(handle, logging.Logger)

        try:
            start_msg = f"INFO: Start {func.__name__} with args={args}, kwargs={kwargs}\n"
            if is_logger:
                handle.info(f"Start {func.__name__} with args={args}, kwargs={kwargs}")
            else:
                handle.write(start_msg)
                if hasattr(handle, 'flush'):
                    handle.flush()


            result = func(*args, **kwargs)

            end_msg = f"INFO: Finished {func.__name__} with result={result}\n"
            if is_logger:
                handle.info(f"Finished {func.__name__} with result={result}")
            else:
                handle.write(end_msg)
                if hasattr(handle, 'flush'):
                    handle.flush()

            return result

        except Exception as e:
            err_msg = f"ERROR: Function {func.__name__} raised {type(e).__name__}: {str(e)}\n"
            if is_logger:
                handle.error(f"Function {func.__name__} raised {type(e).__name__}: {str(e)}")
            else:
                handle.write(err_msg)
                if hasattr(handle, 'flush'):
                    handle.flush()
            raise

    return inner