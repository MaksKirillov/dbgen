import argparse
import random
import string
import textwrap
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

from mimesis import Person
from mimesis import Locale
from mimesis import Gender
from mimesis import Address
from mimesis import Transport
from mimesis import Text
from mimesis.builtins import RussiaSpecProvider

def transpose(matrix: list) -> list:
    """Транспонирование матрицы"""
    return [[matrix[a][b] for a in range(len(matrix))] for b in range(len(matrix[0]))]


def set_genders(num: int) -> list:
    """Устанавливаем пол"""
    gender_column = []
    for _ in range(num): gender_column.append(random.choice(['F', 'M']))
    return gender_column


def get_locale_from_str(lng: str) -> Locale:
    """Определяем язык"""
    language_lower = lng.lower()
    match language_lower:
        case 'ar': return Locale.AR_AE      #Arabic
        case 'ar-ae': return Locale.AR_AE   #Arabic U.A.E
        case 'ar-dz': return Locale.AR_DZ   #Arabic Algeria
        case 'ar-eg': return Locale.AR_EG   #Arabic Egypt
        case 'ar-jo': return Locale.AR_JO   #Arabic Jordan
        case 'ar-om': return Locale.AR_OM   #Arabic Oman
        case 'ar-sy': return Locale.AR_SY   #Arabic Syria
        case 'ar-ye': return Locale.AR_YE   #Arabic Yemen
        case 'cs' : return Locale.CS        #Czech
        case 'da': return Locale.DA         #Danish
        case 'de': return Locale.DE         #German
        case 'de-at': return Locale.DE_AT   #Austrian German
        case 'de-ch': return Locale.DE_CH   #Swiss German
        case 'el': return Locale.EL         #Greek
        case 'en': return Locale.EN         #English
        case 'en-au': return Locale.EN_AU   #Australian English
        case 'en-ca': return Locale.EN_CA   #Canadian English
        case 'en-gb': return Locale.EN_GB   #British English
        case 'es': return Locale.ES         #Spanish
        case 'es-mx': return Locale.ES_MX   #Mexican Spanish
        case 'et': return Locale.ET         #Estonian
        case 'fa': return Locale.FA         #Farsi
        case 'fi': return Locale.FI         #Finnish
        case 'fr': return Locale.FR         #French
        case 'hr': return Locale.HR         #Croatian
        case 'hu': return Locale.HU         #Hungarian
        case 'is': return Locale.IS         #Icelandic
        case 'it': return Locale.IT         #Italian
        case 'ja': return Locale.JA         #Japanese
        case 'kk': return Locale.KK         #Kazakh
        case 'ko': return Locale.KO         #Korean
        case 'nl': return Locale.NL         #Dutch
        case 'nl-be': return Locale.NL_BE   #Belgium Dutch
        case 'no': return Locale.NO         #Norwegian
        case 'pl': return Locale.PL         #Polish
        case 'pt': return Locale.PT         #Portuguese
        case 'pt-br': return Locale.PT_BR   #Brazilian Portuguese
        case 'ru': return Locale.RU         #Russian
        case 'sk': return Locale.SK         #Slovak
        case 'sv': return Locale.SV         #Swedish
        case 'tr': return Locale.TR         #Turkish
        case 'uk': return Locale.UK         #Ukrainian
        case 'zh': return Locale.ZH         #Chinese
        case _: return Locale.EN            #Default English


def get_gender_column(attribute: str, gender_column: list, lng: str) -> list:
    """Получаем столбик с полом"""
    parsed_attributes = attribute.split('_')
    data_column = []
    if len(parsed_attributes) == 1:
        if lng.lower() == 'ru':
            for gender in gender_column:
                if gender == 'F': data_column.append('Ж')
                else:             data_column.append('М')
        else:
            for gender in gender_column:
                if gender == 'F': data_column.append('F')
                else:             data_column.append('M')
    else:
        if lng.lower() == 'ru':
            for gender in gender_column:
                if gender == 'F': data_column.append('Женщина')
                else:             data_column.append('Мужчина')
        else:
            for gender in gender_column:
                if gender == 'F': data_column.append('Female')
                else:             data_column.append('Male')
    return data_column


def get_names_column(attribute: str, gender_column: list, lng: str) -> list:
    """Получаем список имён согласно значению аттрибута"""
    parsed_attributes = attribute.split('_')
    data_column = []
    locale = get_locale_from_str(lng)
    person = Person(locale=locale)
    ru = RussiaSpecProvider()

    # полное имя
    if len(parsed_attributes) == 1 or attribute == 'name_full':
        if lng == 'ru':
            for gender in gender_column:
                if gender == 'F':
                    name = person.first_name(gender=Gender.FEMALE).strip() + ' ' +\
                           ru.patronymic(gender=Gender.FEMALE).strip() + ' ' +\
                           person.last_name(gender=Gender.FEMALE).strip()
                else:
                    name = person.first_name(gender=Gender.MALE).strip() + ' ' +\
                           ru.patronymic(gender=Gender.MALE).strip() + ' ' +\
                           person.last_name(gender=Gender.MALE).strip()
                data_column.append(name)
        else:
            for gender in gender_column:
                if gender == 'F':
                    name = person.full_name(gender=Gender.FEMALE).strip()
                else:
                    name = person.full_name(gender=Gender.MALE).strip()
                data_column.append(name)
    # имя имеет другой формат
    else:
        if lng == 'ru':
            for gender in gender_column:
                name = ''
                if gender == 'F':
                    for name_part in parsed_attributes:
                        match name_part:
                            case 'name':
                                pass
                            case 'first':
                                name = name + person.first_name(gender=Gender.FEMALE).strip() + ' '
                            case 'last':
                                name = name + person.last_name(gender=Gender.FEMALE).strip() + ' '
                            case 'patronymic':
                                name = name + ru.patronymic(gender=Gender.FEMALE).strip() + ' '
                            case _:
                                pass
                else:
                    for name_part in parsed_attributes:
                        match name_part:
                            case 'name':
                                pass
                            case 'first':
                                name = name + person.first_name(gender=Gender.MALE).strip() + ' '
                            case 'last':
                                name = name + person.last_name(gender=Gender.MALE).strip() + ' '
                            case 'patronymic':
                                name = name + ru.patronymic(gender=Gender.MALE).strip() + ' '
                            case _:
                                pass
                data_column.append(name.strip())
        else:
            for gender in gender_column:
                name = ''
                if gender == 'F':
                    for name_part in parsed_attributes:
                        match name_part:
                            case 'name':
                                pass
                            case 'first':
                                name = name + person.first_name(gender=Gender.FEMALE).strip() + ' '
                            case 'last':
                                name = name + person.last_name(gender=Gender.FEMALE).strip() + ' '
                            case 'patronymic':
                                name = name + person.first_name(gender=Gender.MALE).strip() + ' '
                            case _:
                                pass
                else:
                    for name_part in parsed_attributes:
                        match name_part:
                            case 'name':
                                pass
                            case 'first':
                                name = name + person.first_name(gender=Gender.MALE).strip() + ' '
                            case 'last':
                                name = name + person.last_name(gender=Gender.MALE).strip() + ' '
                            case 'patronymic':
                                name = name + person.first_name(gender=Gender.MALE).strip() + ' '
                            case _:
                                pass
                data_column.append(name.strip())

    return data_column


def get_address_columns(attribute: str, num: int, lng: str) -> list:
    """Получаем адреса мест согласно значению аттрибута"""
    parsed_attributes = attribute.split('_')
    data_column = []
    locale = get_locale_from_str(lng)
    address = Address(locale=locale)

    # полное название
    # address_country_city_street_num_1_10
    if len(parsed_attributes) == 1 or attribute == 'address_full':
        for _ in range(num):
            place = address.country().strip() + ', ' +\
                    address.city().strip() + ', ' +\
                    address.street_name().strip() + ', ' +\
                    str(random.randint(1, 10))
            data_column.append(place)
    else:
        for _ in range(num):
            place = ''
            j = 0
            for place_part in parsed_attributes:
                match place_part:
                    case 'place':
                        pass
                    case 'continent':
                        place = place + address.continent().strip() + ', '
                    case 'country':
                        place = place + address.country().strip() + ', '
                    case 'city':
                        place = place + address.city().strip() + ', '
                    case 'street':
                        place = place + address.street_name().strip() + ', '
                    case 'num':
                        place = place + str(
                            random.randint(int(parsed_attributes[j + 1]), int(parsed_attributes[j + 2]))) + ', '
                    case _:
                        pass
                j = j + 1
            data_column.append(place.strip().rstrip(','))

    return data_column


def get_email_column(attribute: str, num: int, lng: str) -> list:
    """Получаем электронные почты согласно значению атрибута"""
    parsed_attributes = attribute.split('_')
    data_column = []
    locale = get_locale_from_str(lng)
    person = Person(locale=locale)

    for _ in range(num):
        if len(parsed_attributes) > 1:
            domain = parsed_attributes[1].lstrip('@')
            data_column.append(person.email(domains=[domain]))
        else:
            data_column.append(person.email())

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
    person = Person(locale=Locale.EN)

    data_column = []
    country_code = '7'
    region_code = '987'
    if len(attribute.split('_')) == 1:
        pass
    else:
        country_code = attribute.split('_')[1]
        region_code = attribute.split('_')[2]

    for _ in range(num):
        if len(attribute.split('_')) != 1:
            if attribute.split('_')[1] == 'r': country_code = random.choice('123456789')
            if attribute.split('_')[2] == 'r': region_code = ''.join(random.choices('123456789', k=3))
        else:
            country_code = random.choice('123456789')
            region_code = ''.join(random.choices('123456789', k=3))

        data_column.append(person.phone_number(mask=f"{country_code}-({region_code})-###-####"))

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


def get_car_column(attribute: str, num:int, lng:str) -> list:
    """Возвращаем лист моделей авто, номеров авто или производителей"""
    data_column = []
    locale = get_locale_from_str(lng)
    transport = Transport()

    if '_' in attribute:
        if attribute.split('_')[1] == 'brand':
            for _ in range(num):
                data_column.append(transport.car())
        elif attribute.split('_')[1] == 'number':
            for _ in range(num):
                data_column.append(transport.vehicle_registration_code(locale=locale))
        elif attribute.split('_')[1] == 'manufacturer':
            for _ in range(num):
                data_column.append(transport.manufacturer())
        else:
            for _ in range(num):
                data_column.append(transport.car())
    else:
        for _ in range(num):
            data_column.append(transport.car())

    return data_column


def get_airplane_column(num:int) -> list:
    """Возвращаем лист моделей самолётов"""
    data_column = []
    transport = Transport()

    for _ in range(num):
        data_column.append(transport.airplane())

    return data_column


def get_education_column(num: int, lng: str) -> list:
    """Получаем электронные почты согласно значению атрибута"""
    data_column = []
    locale = get_locale_from_str(lng)
    person = Person(locale=locale)

    for _ in range(num):
        data_column.append(person.university())

    return data_column


def get_occupation_column(num: int, lng: str) -> list:
    """Получаем электронные почты согласно значению атрибута"""
    data_column = []
    locale = get_locale_from_str(lng)
    person = Person(locale=locale)

    for _ in range(num):
        data_column.append(person.occupation())

    return data_column


def get_color_column(num: int, lng: str) -> list:
    """Получаем список цветов"""
    data_column = []
    locale = get_locale_from_str(lng)
    text = Text(locale=locale)

    for _ in range(num):
        data_column.append(text.color())

    return data_column


def get_bic_column(num: int) -> list:
    """Получаем список БИК"""
    data_column = []
    ru = RussiaSpecProvider()

    for _ in range(num):
        data_column.append(ru.bic())

    return data_column


def get_inn_column(num: int) -> list:
    """Получаем список ИНН"""
    data_column = []
    ru = RussiaSpecProvider()

    for _ in range(num):
        data_column.append(ru.inn())

    return data_column


def get_kpp_column(num: int) -> list:
    """Получаем список КПП"""
    data_column = []
    ru = RussiaSpecProvider()

    for _ in range(num):
        data_column.append(ru.kpp())

    return data_column


def get_ogrn_column(num: int) -> list:
    """Получаем список ОГРН"""
    data_column = []
    ru = RussiaSpecProvider()

    for _ in range(num):
        data_column.append(ru.ogrn())

    return data_column


def get_snils_column(num: int) -> list:
    """Получаем список СНИЛС"""
    data_column = []
    ru = RussiaSpecProvider()

    for _ in range(num):
        data_column.append(ru.snils())

    return data_column


def get_postal_column(num: int, lng: str) -> list:
    """Получаем список почтовых кодов"""
    data_column = []
    locale = get_locale_from_str(lng)
    address = Address(locale=locale)

    for _ in range(num):
        data_column.append(address.postal_code())

    return data_column


def get_passport_column(attribute: str, num:int) -> list:
    """Возвращаем лист моделей авто, номеров авто или производителей"""
    data_column = []
    ru = RussiaSpecProvider()

    if '_' in attribute:
        if attribute.split('_')[1] == 'number':
            for _ in range(num):
                data_column.append(ru.passport_number())
        elif attribute.split('_')[1] == 'series':
            for _ in range(num):
                data_column.append(ru.passport_series())
        else:
            for _ in range(num):
                data_column.append(ru.series_and_number())
    else:
        for _ in range(num):
            data_column.append(ru.series_and_number())

    return data_column


def remove_random_elements(data_column: list, blank_percentage: int) -> list:
    """Убираем рандомные элементы в списке процентно"""
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
            case 'address': data_column = get_address_columns(attribute, num, lng)
            case 'email': data_column = get_email_column(attribute, num, lng)
            case 'date': data_column = get_date_column(attribute, num)
            case 'phone': data_column = get_phone_column(attribute, num)
            case 'gender': data_column = get_gender_column(attribute, genders, lng)
            case 'int': data_column = get_int_column(attribute, num)
            case 'float': data_column = get_float_column(attribute, num)
            case 'boolean': data_column = get_boolean_column(attribute, num)
            case 'string': data_column = get_string_column(attribute, num)
            case 'car': data_column = get_car_column(attribute, num, lng)
            case 'airplane': data_column = get_airplane_column(num)
            case 'education': data_column = get_education_column(num, lng)
            case 'occupation': data_column = get_occupation_column(num, lng)
            case 'color': data_column = get_color_column(num, lng)
            case 'bic': data_column = get_bic_column(num)
            case 'inn': data_column = get_inn_column(num)
            case 'kpp': data_column = get_kpp_column(num)
            case 'ogrn': data_column = get_ogrn_column(num)
            case 'snils': data_column = get_snils_column(num)
            case 'postal': data_column = get_postal_column(num, lng)
            case 'passport': data_column = get_passport_column(attribute, num)
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
                                    address_continent - континент;
                                    address_country - страна;
                                    address_city - город;
                                    address_street - название улицы;
                                    address_num_n1_n2 - случайный номер улицы от n1 до n2;
                                    address_country_city_street_num_n1_n2 - пример совмещения для получения
                                                                          полного названия;
                                    address или address_full - другой вариант полного названия;
                                    -------------------------------
                                    email - электронная почта с разными случайными доменами;
                                    email_mail.ru - адрес почты заканчивается на домен @mail.ru
                                    -------------------------------
                                    date - дата от 01.01.2000 до 12.12.2010;
                                    date_dd.mm.yyyy_dd.mm.yyyy - дата от dd.mm.yyyy до dd.mm.yyyy;
                                    -------------------------------
                                    phone - телефон со всеми случайными значениями;
                                    phone_c_r - телефон, где c - код страны, код региона - случайный;
                                        Пример: phone_7_r
                                    phone_r_a - телефон, где a - код зоны, код страны - случайный;
                                        Пример: phone_r_987
                                    phone_r_r - телефон со всеми случайными значениями;
                                    phone_c_a - телефон, где:
                                                    c - код страны
                                                    a - код зоны
                                        Пример: phone_7_987
                                    -------------------------------
                                    gender - пол в виде F/M или М/Ж;
                                    gender_full - пол в виде Female/Male или Мужчина/Женщина
                                    -------------------------------
                                    bic - банковский код;
                                    inn - идентификационный номер налогоплательщика (ИНН)
                                    kpp - код причины постановки на учёт (КПП)
                                    ogrn - основной государственный регистрационный номер (ОГРН)
                                    snils - страховой номер индивидуального лицевого счёта (СНИЛС)
                                    postal - почтовый код 
                                    -------------------------------
                                    passport - серия и номер паспорта
                                    passport_number - номер паспорта
                                    passport_series - серия паспорта
                                    -------------------------------
                                    car_brand - марка авто;
                                    car_number - номер авто;
                                    car_manufacturer - производитель авто;
                                    -------------------------------
                                    airplane - модель самолёта
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
    parser.add_argument('-l', '--language', type=str, help='Язык таблицы базы данных: en - Английский, ru - Русский;')
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
        language = 'en'
    else:
        language = args.language
        if language not in ['ar', 'ar-ae', 'ar-dz', 'ar-eg', 'ar-jo', 'ar-om', 'ar-sy', 'ar-ye', 'cs', 'da', 'de',
                            'de-at', 'de-ch', 'el', 'en', 'en-au', 'en-ca', 'en-gb', 'es', 'es-mx', 'et', 'fa', 'fi',
                            'fr', 'hr', 'hu', 'is', 'it', 'ja', 'kk', 'ko', 'nl', 'nl-be', 'no', 'pl', 'pt', 'pt-br',
                            'ru', 'sk', 'sv', 'tr', 'uk', 'zh']:
            raise ValueError("Неизвестный язык, используйте, например, 'en' или 'ru'")

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
