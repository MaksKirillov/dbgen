import argparse
import os
import textwrap

import numpy as np
import pandas as pd


def get_relationship_df(df1: pd.DataFrame, df2: pd.DataFrame,
                        cols1: list, cols2: list,
                        num: int, rel_type: str) -> pd.DataFrame:
    """Получения таблицы связей dataframe"""
    output_list = []
    match rel_type:
        case 'one_one':
            for i in range(min(len(df1), len(df2), num)):
                row = {**dict(zip(cols1, df1.iloc[i])),
                       **dict(zip(cols2, df2.iloc[i]))}
                output_list.append(row)
        case 'one_many':
            for i in range(min(len(df1), num)):
                num_links = np.random.randint(2, 11)
                matching_records = df2.sample(num_links)
                for _, record in matching_records.iterrows():
                    row = {**dict(zip(cols1, df1.iloc[i])),
                           **dict(zip(cols2, record))}
                    output_list.append(row)
                if len(output_list) >= min(len(df1), num):
                    return pd.DataFrame(output_list[:min(len(df1), num)])
        case 'many_one':
            for i in range(min(len(df2), num)):
                num_links = np.random.randint(2, 11)
                matching_records = df1.sample(num_links)
                for _, record in matching_records.iterrows():
                    row = {**dict(zip(cols1, record)),
                           **dict(zip(cols2, df2.iloc[i]))}
                    output_list.append(row)
                if len(output_list) >= min(len(df2), num):
                    return pd.DataFrame(output_list[:min(len(df2), num)])
        case 'many_many':
            for _ in range(num):
                num_links = np.random.randint(2, 11)
                record_1 = df1.sample(1).iloc[0]
                record_2 = df2.sample(1).iloc[0]
                matching_records_1 = df1.sample(num_links)
                matching_records_2 = df2.sample(num_links)
                for _, record in matching_records_2.iterrows():
                    row = {**dict(zip(cols1, record_1)),
                           **dict(zip(cols2, record))}
                    output_list.append(row)
                for _, record in matching_records_1.iterrows():
                    row = {**dict(zip(cols1, record)),
                           **dict(zip(cols2, record_2))}
                    output_list.append(row)
                if len(output_list) >= num:
                    return pd.DataFrame(output_list[:num])
        case _: raise ValueError('Неизвестный тип связи')

    return pd.DataFrame(output_list)


if __name__ == '__main__':
    """Основное тело консольного приложения"""

    """Описание и аргументы консольного приложения."""
    parser = argparse.ArgumentParser(
        prog='dbrel',
        description=textwrap.dedent('''\
                                        Создание таблиц со случайными связями на основе двух других
                                        -------------------------------
                                        Поддерживаемые типы связей:
                                        one_one - один к одному
                                        one_many - один ко многим
                                        many_one - многие к одному
                                        many_many - многие ко многим
                                        '''),
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-f', '--first', type=str, help='Путь к первой таблице dataframe в формате .feather;')
    parser.add_argument('-s', '--second', type=str, help='Путь ко второй таблице dataframe в формате .feather;')
    parser.add_argument('-o', '--output', type=str, help='Путь сохранения таблицы со связями;')
    parser.add_argument('-t', '--type', type=str, help='Тип связи;')
    parser.add_argument('-k', '--number', type=int, help='Кол-во кортежей в таблице со связями;')
    parser.add_argument('-n1', '--names_1', nargs='+', type=str, help='Названия аттрибутов для связи в первой таблице;')
    parser.add_argument('-n2', '--names_2', nargs='+', type=str, help='Названия аттрибутов для связи во второй таблице;')
    args = parser.parse_args()

    """Проверка аргументов"""

    """Проверка пути к первой таблице dataframe в формате .feather"""

    if args.first is None:
        raise FileNotFoundError('Не указан путь к первой таблице dataframe в формате .feather')
    else:
        try:
            file_first = args.first
            if os.path.isfile(file_first):
                if file_first.endswith('.feather'):
                    pass
                else:
                    raise TypeError('Первый файл должен быть формата .feather и оканчиваться на .feather')
            else:
                raise FileNotFoundError('Первого файла не существует')
        except Exception as error:
            print(f"Произошла ошибка: {error}")

    file_first = args.first
    df_1 = pd.read_feather(file_first)

    """Проверка пути ко второй таблице dataframe в формате .feather"""

    if args.second is None:
        raise FileNotFoundError('Не указан путь ко второй таблице dataframe в формате .feather')
    else:
        try:
            file_second = args.second
            if os.path.isfile(file_second):
                if file_second.endswith('.feather'):
                    pass
                else:
                    raise TypeError('Второй файл должен быть формата .feather и оканчиваться на .feather')
            else:
                raise FileNotFoundError('Второго файла не существует')
        except Exception as error:
            print(f"Произошла ошибка: {error}")

    file_second = args.second
    df_2 = pd.read_feather(file_second)

    """Проверка типа связи"""

    if args.type is None:
        relation_type = 'one_one'
    else:
        relation_type = args.type
        if relation_type not in ['one_one', 'one_many', 'many_one', 'many_many']:
            raise ValueError('Неподдерживаемый формат связи')

    relation_type = args.type

    """Проверка кол-ва кортежей в таблице"""

    if args.number is None:
        number_of_lines = 10
    else:
        number_of_lines = args.number

    if number_of_lines <= 0:
        raise ValueError("Кол-во кортежей должно быть больше 0")


    """Проверка названий атрибутов"""

    if args.names_1 is None and args.names_2 is None:
        attr_names_1 = list(df_1)
        attr_names_2 = list(df_2)
    elif args.names_1 is None:
        attr_names_1 = list(df_1)
        attr_names_2 = args.names_2
    elif args.names_2 is None:
        attr_names_1 = args.names_1
        attr_names_2 = list(df_2)
    else:
        attr_names_1 = args.names_1
        attr_names_2 = args.names_2


    """Получение таблицы связей"""

    df = get_relationship_df(df_1, df_2, attr_names_1, attr_names_2, number_of_lines, relation_type)

    print('Таблица:')
    print(df)
    print()

    """Сохранение таблицы"""

    if args.output is not None:
        try:
            file_name = args.output
            base_name, ext = os.path.splitext(file_name)
            file_name = base_name + '.feather'
            df.to_feather(file_name)
            print(f'Таблица сохранена в формате .feather по адресу: {file_name}')
        except Exception as error:
            print(f"Произошла ошибка: {error}")
