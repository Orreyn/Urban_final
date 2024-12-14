import datetime
import random


def write_words(word_count, file_name):
    """

    Принимает количество слов для записи и наименование файла.
    Записывает в файл строчки в заданном количестве, указывая номер строки в конце.

    """
    file = open(f'Files/{file_name}', 'w+', encoding='utf-8')
    for i in range(word_count + 1):
        file.write(f'Какое-то слово №{i}\n')
    print(f'Завершилась запись в файл {file_name}')


def numbers_write():
    """ Создаёт файл с числами. """
    file = open('Files/Numbers.txt', 'w+', encoding='utf-8')
    for i in range(0, 1999999):
        file.writelines(f'{i}\n')
    file.close()


def number_to_words(num: int) -> str:
    """

    Принимает число.
    Конвертирует полученное число в текстовую строку на английском.

    """
    if num == 0:
        return 'Zero'

    def helper(n):
        """ Перебирает числа и возвращает результат соответственно спискам. """
        if n < 0:
            return 'Minus ' + helper(-n)
        if n == 0:
            return ''
        elif n < 20:
            return below_twenty[n] + ' '
        elif n < 100:
            return tens[n // 10] + ' ' + helper(n % 10)
        else:
            return below_twenty[n // 100] + ' Hundred ' + helper(n % 100)

    below_twenty = ['', 'One', 'Two', 'Three', 'Four', 'Five',
                    'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven',
                    'Twelve', 'Thirteen', 'Fourteen', 'Fifteen',
                    'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
    tens = ['', 'Ten', 'Twenty', 'Thirty', 'Forty', 'Fifty',
            'Sixty', 'Seventy', 'Eighty', 'Ninety']
    thousands = ['', 'Thousand', 'Million', 'Billion']

    result = ''
    i = 0

    while num > 0:
        if num % 1000 != 0:
            result = helper(num % 1000) + thousands[i] + ' ' + result
        num //= 1000
        i += 1

    return result.strip()


def get_birthdays(number_of_birthdays):
    """

    Возвращает список объектов дат для случайных дней рождения.
    Создаёт список дней рождений в формате даты и месяца из календаря.
    Год не принципиален.

    """
    birthdays = []
    for i in range(number_of_birthdays):
        year_start = datetime.date(2001, 1, 1)
        random_number_of_days = datetime.timedelta(random.randint(0, 364))
        birthday = year_start + random_number_of_days
        birthdays.append(birthday)
    return birthdays


def get_match(birthdays):
    """

    Возвращает объект даты дня рождения, встречающегося несколько
    раз в списке дней рождения.

    """
    if len(birthdays) == len(set(birthdays)):
        return None
    for a, birthdayA in enumerate(birthdays):
        """ Сравнивает все дни рождения друг с другом попарно. """
        for b, birthdayB in enumerate(birthdays[a + 1 :]):
            if birthdayA == birthdayB:
                return birthdayA


months = ('Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня',
          'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря')
