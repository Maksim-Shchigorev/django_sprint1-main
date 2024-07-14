# Импортируйте необходимые модули.
from datetime import datetime

# Укажите два параметра функции:


def validate_record(data_str):
    try:
        datetime.strtime(data_str, '%d.%m.%Y')
        return True
    except ValueError:
        return False


def process_people(data):
    # Объявите счётчики.
    counter = 0
    for _, date_str in data:
        if validate_record(date_str):
            counter += 1
    # в каждой паре значений из списка data
    # проверьте корректность формата даты рождения
    # и в зависимости от результата проверки увеличьте один из счётчиков.
    return counter


data = [
    ('Иван Иванов', '10.01.2004'),
    ('Пётр Петров', '15.03.1956'),
    ('Зинаида Зеленая', '6 февраля 1997'),
    ('Елена Ленина', 'Второе мая тысяча девятьсот восемьдесят пятого'),
    ('Кирилл Кириллов', '26/11/2003')
]
statistics = process_people(data)
# Выведите на экран информацию о корректных и некорректных записях
# в таком формате:
print(f'Корректных записей: {process_people(data)}')
# Некорректных записей: <число>
