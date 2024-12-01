import argparse
import random
import string
import textwrap
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta


def transpose(matrix: list) -> list:
    """Транспонирование матрицы"""
    return [[matrix[a][b] for a in range(len(matrix))] for b in range(len(matrix[0]))]


def set_genders(num: int) -> list:
    """Устанавливаем пол"""
    gender_column = []
    for _ in range(num): gender_column.append(random.choice(['F', 'M']))
    return gender_column


def get_gender_column(attribute: str, gender_column: list, lng: str) -> list:
    """Получаем столбик с полом"""
    parsed_attributes = attribute.split('_')
    data_column = []
    if len(parsed_attributes) == 1:
        if lng == 'eng':
            for gender in gender_column:
                if gender == 'F': data_column.append('F')
                else:             data_column.append('M')
        if lng == 'rus':
            for gender in gender_column:
                if gender == 'F': data_column.append('Ж')
                else:             data_column.append('М')
    else:
        if lng == 'eng':
            for gender in gender_column:
                if gender == 'F': data_column.append('Female')
                else:             data_column.append('Male')
        if lng == 'rus':
            for gender in gender_column:
                if gender == 'F': data_column.append('Женщина')
                else:             data_column.append('Мужчина')
    return data_column


def get_names_column(attribute: str, gender_column: list, lng: str) -> list:
    """Получаем имена согласно значению аттрибута"""
    file_first_f, file_first_m, file_last = '', '', ''
    parsed_attributes = attribute.split('_')
    data_column = []
    try:
        file_first_f = open(f'attribute_values/{lng}/name/first_f', 'r', encoding='utf-8')
        file_first_m = open(f'attribute_values/{lng}/name/first_m', 'r', encoding='utf-8')
        file_last = open(f'attribute_values/{lng}/name/last', 'r', encoding='utf-8')

        lines_first_f = file_first_f.readlines()
        lines_first_m = file_first_m.readlines()
        lines_last = file_last.readlines()

        # полное имя
        if len(parsed_attributes) == 1 or attribute == 'name_first_patronymic_last' or attribute == 'name_full':
            if lng == 'eng':
                for gender in gender_column:
                    if gender == 'F':
                        name = random.choice(lines_first_f).strip() + ' ' \
                               + random.choice(lines_first_f).strip() + ' '\
                               + random.choice(lines_last).strip()
                    else:
                        name = random.choice(lines_first_m).strip() + ' ' \
                               + random.choice(lines_first_m).strip() + ' ' \
                               + random.choice(lines_last).strip()
                    data_column.append(name)
            if lng == 'rus':
                for gender in gender_column:
                    if gender == 'F':
                        name = random.choice(lines_first_f).strip() + ' ' \
                               + random.choice(lines_first_m).strip() + 'овна '\
                               + random.choice(lines_last).strip() + 'а'
                    else:
                        name = random.choice(lines_first_m).strip() + ' ' \
                               + random.choice(lines_first_m).strip() + 'ович ' \
                               + random.choice(lines_last).strip()
                    data_column.append(name)
        # имя имеет другой формат
        else:
            if lng == 'eng':
                for gender in gender_column:
                    name = ''
                    if gender == 'F':
                        for name_part in parsed_attributes:
                            match name_part:
                                case 'name': pass
                                case 'first': name = name + random.choice(lines_first_f).strip() + ' '
                                case 'last': name = name + random.choice(lines_last).strip() + ' '
                                case 'patronymic': name = name + random.choice(lines_first_f).strip() + ' '
                                case _: pass
                    else:
                        for name_part in parsed_attributes:
                            match name_part:
                                case 'name': pass
                                case 'first': name = name + random.choice(lines_first_m).strip() + ' '
                                case 'last': name = name + random.choice(lines_last).strip() + ' '
                                case 'patronymic': name = name + random.choice(lines_first_m).strip() + ' '
                                case _: pass
                    data_column.append(name.strip())
            if lng == 'rus':
                for gender in gender_column:
                    name = ''
                    if gender == 'F':
                        for name_part in parsed_attributes:
                            match name_part:
                                case 'name': pass
                                case 'first': name = name + random.choice(lines_first_f).strip() + ' '
                                case 'last': name = name + random.choice(lines_last).strip() + 'а '
                                case 'patronymic': name = name + random.choice(lines_first_f).strip() + 'овна '
                                case _: pass
                    else:
                        for name_part in parsed_attributes:
                            match name_part:
                                case 'name': pass
                                case 'first': name = name + random.choice(lines_first_m).strip() + ' '
                                case 'last': name = name + random.choice(lines_last).strip() + ' '
                                case 'patronymic': name = name + random.choice(lines_first_m).strip() + 'ович '
                                case _: pass
                    data_column.append(name.strip())
    except FileNotFoundError:
        print(f"Файл для аттрибута {lng} {attribute} не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        file_first_f.close()
        file_first_m.close()
        file_last.close()
    return data_column


def get_place_columns(attribute: str, num: int, lng: str) -> list:
    """Получаем адреса мест согласно значению аттрибута"""
    file_country_city, file_street = '', ''
    parsed_attributes = attribute.split('_')
    data_column = []

    try:
        file_country_city = open(f'attribute_values/{lng}/place/country_city', 'r', encoding='utf-8')
        file_street = open(f'attribute_values/{lng}/place/street', 'r', encoding='utf-8')

        lines_country_city = file_country_city.readlines()
        lines_street = file_street.readlines()

        # полное название
        # place_country_city_street_num_1_10
        if len(parsed_attributes) == 1 or attribute == 'place_full':
            for _ in range(num):
                place = random.choice(lines_country_city).strip() + ', ' \
                        + random.choice(lines_street).strip() + ', ' \
                        + str(random.randint(1, 10))
                data_column.append(place)
        else:
            for _ in range(num):
                place = ''
                j = 0
                for place_part in parsed_attributes:
                    match place_part:
                        case 'place': pass
                        case 'country': place = place + random.choice(lines_country_city).split(',')[0].strip() + ', '
                        case 'city': place = place + random.choice(lines_country_city).split(',')[1].strip() + ', '
                        case 'street': place = place + random.choice(lines_street).strip() + ', '
                        case 'num': place = place + str(random.randint(int(parsed_attributes[j + 1]), int(parsed_attributes[j + 2]))) + ', '
                        case _: pass
                    j = j + 1
                data_column.append(place.strip().rstrip(','))
    except FileNotFoundError:
        print(f"Файл для аттрибута {lng} {attribute} не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        file_country_city.close()
        file_street.close()

    return data_column


def generate_random_email(domain: str) -> str:
    """Генерирует случайный адрес электронной почты с заданным доменом."""
    username_length = random.randint(5, 10)
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=username_length))
    return f"{username}@{domain}"

def generate_random_domain() -> str:
    """Создает случайный домен."""
    domain_length = random.randint(3, 10)
    tld_list = ['.com', '.net', '.org', '.ru', '.info', '.xyz']
    domain_name = ''.join(random.choices(string.ascii_lowercase, k=domain_length))
    return f"{domain_name}{random.choice(tld_list)}"


def get_email_column(attribute: str, num: int) -> list:
    """Получаем электронные почты согласно значению атрибута"""
    parsed_attributes = attribute.split('_')
    data_column = []

    for _ in range(num):
        if len(parsed_attributes) > 1:
            domain = parsed_attributes[1].lstrip('@')
        else:
            domain = generate_random_domain()
        data_column.append(generate_random_email(domain))

    return data_column


def get_date_column(attribute: str, num: int) -> list:
    """Получаем даты согласно значению аттрибута"""
    start_date_str, end_date_str = attribute.split('_')[1], attribute.split('_')[2]

    start_date = datetime.strptime(start_date_str, '%d.%m.%Y')
    end_date = datetime.strptime(end_date_str, '%d.%m.%Y')

    if start_date > end_date:
        raise ValueError("Начальная дата больше конечной даты.")

    data_column = []
    for _ in range(num):
        random_days = random.randint(0, (end_date - start_date).days)
        random_date = start_date + timedelta(days=random_days)
        data_column.append(random_date.strftime('%d.%m.%Y'))

    return data_column


def get_phone_column(attribute: str, num: int) -> list:
    """Получаем телефоны согласно значению аттрибута"""
    data_column = []
    num_of_numbers = 7
    country_code = '7'
    region_code = '987'
    if len(attribute.split('_')) == 1:
        pass
    else:
        country_code = attribute.split('_')[1]
        region_code = attribute.split('_')[2]
        if attribute.split('_')[3] != 'r':
            num_of_numbers = int(attribute.split('_')[3])

    for _ in range(num):
        if len(attribute.split('_')) != 1:
            if attribute.split('_')[1] == 'r': country_code = random.choice('123456789')
            if attribute.split('_')[2] == 'r': region_code = ''.join(random.choices('123456789', k=3))
            if attribute.split('_')[3] == 'r': num_of_numbers = int(random.choice('56789'))
        else:
            country_code = random.choice('123456789')
            region_code = ''.join(random.choices('123456789', k=3))
            num_of_numbers = int(random.choice('56789'))

        local_number = ''.join(random.choices('0123456789', k=num_of_numbers))
        phone_number = f"+{country_code} ({region_code}) {local_number}"
        data_column.append(phone_number)

    return data_column


def get_int_column(attribute: str, num: int) -> list:
    """Получаем целые числа согласно значению аттрибута"""
    if '_' in attribute:
        n1, n2 = int(attribute.split('_')[1]), int(attribute.split('_')[2])
    else:
        n1, n2 = 0, 100
    data_column = [random.randint(n1, n2) for _ in range(num)]
    return data_column


def get_float_column(attribute: str, num: int) -> list:
    """Получаем нецелые числа согласно значению аттрибута"""
    if '_' in attribute:
        n1, n2 = float(attribute.split('_')[1]), float(attribute.split('_')[2])
    else:
        n1, n2 = 0.0, 1.0
    data_column = [random.uniform(n1, n2) for _ in range(num)]
    return data_column

def get_boolean_column(attribute: str, num: int) -> list:
    """Получаем логику True/False согласно значению аттрибута"""
    if '_' not in attribute:
        return [random.choice([True, False]) for _ in range(num)]
    else:
        _, pr = attribute.split('_')
        pr = int(pr)
        if 0 <= pr <= 100:
            return [random.random() < (pr / 100) for _ in range(num)]
        else:
            raise ValueError("Вероятность должна быть в диапазоне от 0 до 100")


def get_string_column(attribute: str, num: int) -> list:
    """Получаем строки согласно значению аттрибута"""
    if '_' in attribute:
        n1, n2 = int(attribute.split('_')[1]), int(attribute.split('_')[2])
    else:
        n1, n2 = 10, 20

    if n1 < 1 or n2 < n1:
        raise ValueError("n1 должен быть больше или равен 1, а n2 должен быть больше n1")

    data_column = []
    for _ in range(num):
        length = random.randint(n1, n2)  # Случайная длина строки от n1 до n2
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        data_column.append(random_string)

    return data_column


def get_file_column(path: str, num: int, lng: str) -> list:
    """Получаем названия из файла"""
    file = ''
    data_column = []

    try:
        file = open(f'attribute_values/{lng}/{path}', 'r', encoding='utf-8')
        lines_file = file.readlines()
        for _ in range(num): data_column.append(random.choice(lines_file).strip())
    except FileNotFoundError:
        print(f"Файл для аттрибута {lng} animal name не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        file.close()

    return data_column


def remove_random_elements(data_column: list, blank_percentage: int) -> list:
    num_to_remove = int(len(data_column) * (blank_percentage / 100))
    indices_to_remove = np.random.choice(len(data_column), num_to_remove, replace=False)
    modified_data_column = data_column.copy()
    for index in indices_to_remove:
        modified_data_column[index] = None
    return modified_data_column


def get_generated_data(attributes: list, num: int, lng: str, blanks: list) -> list:
    """Генерирует данные для таблицы"""
    data = []
    genders = set_genders(num)
    for attribute, blank_pr in zip(attributes, blanks):
        parsed_attributes = attribute.split('_')
        match parsed_attributes[0]:
            case 'name': data_column = get_names_column(attribute, genders, lng)
            case 'place': data_column = get_place_columns(attribute, num, lng)
            case 'email': data_column = get_email_column(attribute, num)
            case 'date': data_column = get_date_column(attribute, num)
            case 'phone': data_column = get_phone_column(attribute, num)
            case 'gender': data_column = get_gender_column(attribute, genders, lng)
            case 'int': data_column = get_int_column(attribute, num)
            case 'float': data_column = get_float_column(attribute, num)
            case 'boolean': data_column = get_boolean_column(attribute, num)
            case 'string': data_column = get_string_column(attribute, num)
            case 'animal':
                if parsed_attributes[1] == 'name': data_column = get_file_column('animal/name', num, lng)
                elif parsed_attributes[1] == 'species': data_column = get_file_column('animal/species', num, lng)
                else: raise TypeError('Нет такого типа у аттрибутов animal')
            case 'car': data_column = get_file_column('car_brand', num, lng)
            case 'education': data_column = get_file_column('education', num, lng)
            case 'occupation': data_column = get_file_column('occupation', num, lng)
            case 'color': data_column = get_file_column('color', num, lng)
            case _: raise TypeError(f'Нет типа {parsed_attributes[0]} у аттрибутов')
        data.append(remove_random_elements(data_column, blank_pr))
    return transpose(data)


if __name__ == '__main__':
    """Основное тело консольного приложения"""

    """Описание и аргументы консольного приложения."""
    parser = argparse.ArgumentParser(
        prog='dbgen',
        description=textwrap.dedent('''\
                                    Генератор тестовых данных для таблицы базы данных
                                    -------------------------------
                                    Есть следующие типы аттрибутов:
                                    name_first - только имя;
                                    name_last - только фамилия;
                                    name_patronymic - отчество/среднее имя в зависимости от языка;
                                    name_first_patronymic_last - пример совмещения для получения
                                                                 полного имени;
                                    name или name_full - другой вариант полного имени;
                                    -------------------------------
                                    place_country - страна;
                                    place_city - город;
                                    place_street - название улицы;
                                    place_num_n1_n2 - случайный номер улицы от n1 до n2;
                                    place_country_city_street_num_n1_n2 - пример совмещения для получения
                                                                          полного названия;
                                    place или place_full - другой вариант полного названия;
                                    -------------------------------
                                    email - электронная почта с разными случайными доменами;
                                    email_@mail.ru - адрес почты заканчивается на домен @mail.ru
                                    -------------------------------
                                    date - дата от 01.01.2000 до 12.12.2010;
                                    date_dd.mm.yyyy_dd.mm.yyyy - дата от dd.mm.yyyy до dd.mm.yyyy;
                                    -------------------------------
                                    phone - телефон со всеми случайными значениями;
                                    phone_c_r_r - телефон, где c - код страны, код региона - случайный;
                                    phone_r_a_r - телефон, где a - код зоны, код страны - случайный;
                                    phone_r_r_n - телефон, n - кол-во цифр после кодов, коды - случайный;
                                    phone_r_r_r - телефон со всеми случайными значениями;
                                    phone_c_a_n - телефон, где:
                                                    c - код страны
                                                    a - код зоны
                                                    n - кол-во цифр после кодов;
                                    -------------------------------
                                    gender - пол в виде F/M или М/Ж;
                                    gender_full - пол в виде Female/Male или Мужчина/Женщина
                                    -------------------------------
                                    animal_name - кличка животного;
                                    animal_species - вид животного;
                                    ------------------------------
                                    car_brand - марка авто;
                                    car_number - номер авто;
                                    -------------------------------
                                    education - место образования;
                                    occupation - место работы;
                                    -------------------------------
                                    color - цвет;
                                    -------------------------------   
                                    int - целое число от 0 до 100;
                                    int_n1_n2 - целое число от n1 до n2;
                                    float - нецелое число от 0 до 1;
                                    float_n1_n2 - нецелое число от n1 до n2;
                                    boolean - логика true/false, true появляется в 50% случаях
                                    boolean_pr - логика true/false, true появляется в pr% случаях
                                    string - случайная надпись длиной от 10 до 20
                                    string_n1_n2 - случайная надпись длиной от n1 до n2
                                    -------------------------------
                                    '''),
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-n', '--names', nargs='+', type=str, help='Названия аттрибутов в таблице, массив str;')
    parser.add_argument('-t', '--types', nargs='+', type=str, help='Типы аттрибутов в таблице, массив str;')
    parser.add_argument('-l', '--language', type=str, help='Язык таблицы базы данных: eng - Английский, rus - Русский;')
    parser.add_argument('-k', '--number',  type=int, help='Количество кортежей в таблице базы данных, int;')
    parser.add_argument('-b', '--blank', nargs='+', type=int, help='Процент пустых данных от 0 до 100;')
    parser.add_argument('-s', '--save', type=str, help='Сохранить таблицу в формате .feather по указанному пути.')
    args = parser.parse_args()

    """Проверка аргументов"""

    """Проверка кол-ва кортежей в таблице"""

    if args.number is None:
        number_of_lines = 10
    else:
        number_of_lines = args.number

    if number_of_lines <= 0:
        raise ValueError("Кол-во кортежей должно быть больше 0")


    """Проверка аргумента - язык БД"""

    if args.language is None:
        language = 'eng'
    else:
        language = args.language
        if language not in ['rus', 'eng']:
            raise ValueError("Неизвестный язык, используйте 'eng' или 'rus'")

    """Проверка названий и типов аттрибутов"""

    if args.names is None and args.types is None:
        attr_names = ['name','phone','email']
        attr_types = ['name_full','phone','email']
    elif args.names is None:
        raise ValueError("Нет названий аттрибутов")
    elif args.types is None:
        raise ValueError("Нет типов аттрибутов")
    else:
        attr_names = args.names
        attr_types = args.types

    if len(attr_names) != len(attr_types):
        raise ValueError("Кол-во названий и типов аттрибутов должно совпадать")


    """Проверка процентов пустых данных"""

    blank = []
    if args.blank is None:
        for i in range(number_of_lines):
            blank.append(0)
    elif len(args.blank) == 1:
        for i in range(number_of_lines):
            blank.append(int(args.blank[0]))
    elif len(args.blank) != len(attr_names):
        raise ValueError("""
                            Кол-во названий и кол-во разных процентов пустых данных должно совпадать или
                            кол-во процентов должно равняться 1
                            """)
    else:
        for blank_part in blank:
            if not 0 <= blank_part <= 100:
                raise ValueError("Один из процентов пустых данных не попадает в значение между 0 и 100")


    """Создание таблицы"""

    df = pd.DataFrame(get_generated_data(attr_types, number_of_lines, language, blank), columns=attr_names)

    print('Таблица:')
    print(df)
    print()


    """Сохранение таблицы"""

    if args.save is not None:
        try:
            file_name = args.save
            base_name, ext = os.path.splitext(file_name)
            file_name = base_name + '.feather'
            df.to_feather(file_name)
            print(f'Таблица сохранена в формате .feather по адресу: {file_name}')
        except Exception as error:
            print(f"Произошла ошибка: {error}")
