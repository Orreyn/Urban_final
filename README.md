# Urban_final
В данном проекте выполняются задачи тремя разными подходами - Threading, Multiprocessing и asyncio - и сравниваются по результативности работы. Главными показателями сравнения являются время работы кода и нагрузка на оперативную память.

Пример кода второй задачи, выполненной через Threads.
```Python
"""Задача 2"""
import threading
import time
import math
import sqlite3
from typing import List
import psutil

lock = threading.Lock()
cpu = psutil.Process()
N_JOBS = 4
LOAD = 100_000_000

rdb = sqlite3.connect('Database/Result.db')
cursor = rdb.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS ThreadsResults(
task INTEGER NOT NULL PRIMARY KEY,
time FLOAT NOT NULL,
memory TEXT NOT NULL
)
''')


def summer(arr: List[int], i: int, summ: List[int], lock: threading.Lock) -> None:
    """

    Суммирует часть квадратных корней последовательности
    из 100000000 чисел (LOAD), полученную за счёт деления
    последовательности на N_JOBS частей.

    """
    begin = int(i * LOAD / N_JOBS)
    end = int((i + 1) * LOAD / N_JOBS)
    res = 0
    for k in range(begin, end):
        res += math.sqrt(arr[k])
    with lock:
        summ[i] = res


def task_2():
    """

    Вызывает функцию summer.
    Создаёт потоки для выполнения функции N_JOBS раз параллельно.
    Вычисляет время работы функции и её нагрузку на память.
    Заносит результаты вычислений в базу данных.

    """
    started_at = time.time()
    arr = list(range(LOAD))
    summ = [0] * N_JOBS
    threads = [None] * N_JOBS
    for i in range(N_JOBS):
        threads[i] = threading.Thread(target=summer, args=(arr, i, summ, lock))
        threads[i].start()
    for i in range(N_JOBS):
        threads[i].join()
    print(f'Резуальтат: {sum(summ)}')
    ended_at = time.time()
    elapsed = round(ended_at - started_at, 6)
    memories = f'{round(cpu.memory_percent(), 6)}%'
    print(f'Время работы: {elapsed} секунд')
    print(f'Нагрузка на память: {memories}')
    cursor.execute('INSERT or REPLACE INTO ThreadsResults (task, time, memory) '
                   'VALUES (?, ?, ?)', (2, f'{elapsed}', f'{memories}'))


task_2()
rdb.commit()
rdb.close()

```

Результат работы:
```
Резуальтат: 666666661666.5139
Время работы: 6.153496 секунд
Нагрузка на память: 11.959611%
