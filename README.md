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
```

Пример кода вывода работы всех подходов со всеми задачами:
```Python
"""Главный файл, в котором вызываются результаты всех остальных и создаётся база данных для их записи"""

import sqlite3

rdb = sqlite3.connect('Database/Result.db')
cursor = rdb.cursor()

""" Вывод результатов работы всех модулей по времени и нагрузке. """
print(f'Время выполнения (в секундах) и нагрузка (в процентах) '
      f'каждой задачи с использованием потоков:')
cursor.execute('SELECT task, time, memory FROM ThreadsResults GROUP BY task')
t_results = cursor.fetchall()
for result in t_results:
    print(f'Задача номер: {result[0]}, время: {result[1]}, нагрузка: {result[2]}')
print('')

print(f'Время выполнения (в секундах) и нагрузка (в процентах) '
      f'каждой задачи с использованием процессов:')
cursor.execute('SELECT task, time, memory FROM MultiResults GROUP BY task')
m_results = cursor.fetchall()
for result in m_results:
    print(f'Задача номер: {result[0]}, время: {result[1]}, нагрузка: {result[2]}')
print('')

print(f'Время выполнения (в секундах) и нагрузка (в процентах) '
      f'каждой задачи с использованием асинхронности:')
cursor.execute('SELECT task, time, memory FROM asyncResults GROUP BY task')
a_results = cursor.fetchall()
for result in a_results:
    print(f'Задача номер: {result[0]}, время: {result[1]}, нагрузка: {result[2]}')
```

Результат работы:
```
Время выполнения (в секундах) и нагрузка (в процентах) каждой задачи с использованием потоков:
Задача номер: 1, время: 1.973039, нагрузка: 0.0703%
Задача номер: 2, время: 7.533068, нагрузка: 11.825803%
Задача номер: 3, время: 6.002116, нагрузка: 0.076947%
Задача номер: 4, время: 8.41999, нагрузка: 0.321407%
Задача номер: 5, время: 505.906264, нагрузка: 0.090853%

Время выполнения (в секундах) и нагрузка (в процентах) каждой задачи с использованием процессов:
Задача номер: 1, время: 0.588001, нагрузка: 0.076131%
Задача номер: 2, время: 22.435028, нагрузка: 11.836949%
Задача номер: 3, время: 6.097704, нагрузка: 0.091225%
Задача номер: 4, время: 4.822562, нагрузка: 0.334917%
Задача номер: 5, время: 90.784, нагрузка: 0.101016%

Время выполнения (в секундах) и нагрузка (в процентах) каждой задачи с использованием асинхронности:
Задача номер: 1, время: 1.955002, нагрузка: 0.114935%
Задача номер: 2, время: 13.581589, нагрузка: 0.118474%
Задача номер: 3, время: 6.002367, нагрузка: 0.11851%
Задача номер: 4, время: 9.068018, нагрузка: 0.133964%
Задача номер: 5, время: 600.249267, нагрузка: 0.134276%
