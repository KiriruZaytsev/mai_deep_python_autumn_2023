import json
from time import time, sleep
from functools import wraps
from random import randint
from collections import deque
from contextlib import contextmanager


@contextmanager
def timer():
    '''
    Функция-таймер
    '''
    start_time = time()
    end_time = 0.0
    yield lambda: (end_time or time()) - start_time
    end_time = time()

def mean(k):
    '''
    Декоратор, позволяющий вычислять среднее время
    последних k вызовов функции
    '''
    def inner(func):
        '''
        Т.к. декоратор должен принимать в качестве аргумента
        количество вызовов, создадим новый декоратор, который
        будет принимать функцию func
        '''
        execution_times = deque()
        sum_k = 0.0

        @wraps(func)
        def wrapper(*args, **kwargs):
            '''
            Часть, вычисляющая среднее время последних k вызовов
            '''
            nonlocal execution_times
            nonlocal sum_k

            with timer() as exec_time:
                result = func(*args, **kwargs)

            if len(execution_times) >= k:
                dropped = execution_times.popleft()
                sum_k -= dropped

            cur_time = exec_time()
            execution_times.append(cur_time)
            sum_k += cur_time

            print(sum_k / len(execution_times))

            return result
        return wrapper
    return inner


def callback(field, key):
    '''
    Функция-обработчик полученных в результате парсинга результатов.
    Для демонстрации корректной работы декоратора, используется sleep
    '''
    print(f'{field}, {key}')
    sleep(randint(0, 2))

@mean(5)
def parse_json(json_str: str, keyword_callback, required_fields = None, keywords = None):

    '''
    Функция, с помощью которой осуществляется парсинг строки
    '''

    if keyword_callback is None:
        raise TypeError("Функция-обработчик должна быть явно указана")

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        raise ValueError("Введено неверное имя строки JSON")

    if required_fields is None:
        for field in data:
            if keywords is None:
                first_word, second_word = data[field].split()
                keyword_callback(field, first_word)
                keyword_callback(field, second_word)
            else:
                for key in keywords:
                    if key in data[field]:
                        keyword_callback(field, key)
    else:
        for field in required_fields:
            if keywords is None:
                first_word, second_word = data[field].split()
                keyword_callback(field, first_word)
                keyword_callback(field, second_word)
            else:
                for key in keywords:
                    if key in data[field]:
                        keyword_callback(field, key)

def main():
    '''
    Пример работы программы
    '''
    json_str = '''
    {
        "key1": "word1 word2",
        "key2": "word2 word3"
    }
    '''
    for i in range(20):
        parse_json(json_str, callback)
        print(f"= {i} mean time of 5 last executions")
    time()

if __name__ == "__main__":
    main()