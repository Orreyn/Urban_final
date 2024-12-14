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