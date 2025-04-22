import argparse
import os
import textwrap
import pandas as pd


def df_to_sql(data_frame: pd.DataFrame, file_path: str, table_name: str):
    """Создание скрипта на языке Oracle SQL"""
    with open(file_path, 'w', encoding="utf-8") as file:
        sql_script = f"CREATE TABLE {table_name} (\n"

        data_types = {
            'int64': 'NUMBER',
            'float64': 'FLOAT',
            'object': 'VARCHAR2(255)',
            'bool': 'VARCHAR2(5)',
        }

        for column in data_frame.columns:
            column_type = data_types.get(str(data_frame[column].dtype), 'VARCHAR2(255)')
            sql_script += f"    {column} {column_type},\n"

        sql_script = sql_script.rstrip(',\n') + "\n);\n\n"
        file.write(sql_script)

        for index, row in data_frame.iterrows():
            values = []
            for value in row:
                if pd.isnull(value):
                    values.append('NULL')
                elif isinstance(value, str):
                    value = value.replace("'", "''")
                    values.append(f"'{value}'")
                elif isinstance(value, bool):
                    values.append(f"'{value}'")
                else:
                    values.append(str(value))

            insert_statement = f"INSERT INTO {table_name} ({', '.join(data_frame.columns)}) VALUES ({', '.join(values)});\n"
            file.write(insert_statement)


if __name__ == '__main__':
    """Основное тело консольного приложения"""

    """Описание и аргументы консольного приложения."""
    parser = argparse.ArgumentParser(
        prog='dbsaver',
        description=textwrap.dedent('''\
                                        Сохранение dataframe в формате .feather в другом формате
                                        -------------------------------
                                        Поддерживаемые форматы:
                                        csv - Comma-Separated Values - значения, разделённые запятыми;
                                        xlsx - формат Excel;
                                        xml - eXtensible Markup Language - расширяемый язык разметки;
                                        json - JavaScript Object Notation;
                                        html - Hyper Text Markup Language
                                        sql - скрипт sql на создание и заполнение таблицы;
                                        '''),
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-i', '--input', type=str, help='Путь к таблице dataframe в формате .feather;')
    parser.add_argument('-o', '--output', type=str, help='Путь сохранения таблицы в другом формате;')
    parser.add_argument('-f', '--format', type=str, help='Формат сохранения.')
    args = parser.parse_args()

    """Проверка аргументов"""

    """Проверка пути к таблице dataframe в формате .feather"""

    if args.input is None:
        raise FileNotFoundError('Не указан путь к таблице dataframe в формате .feather')
    else:
        try:
            file_input = args.input
            if os.path.isfile(file_input):
                if file_input.endswith('.feather'):
                    pass
                else:
                    raise TypeError('Файл должен быть формата .feather и оканчиваться на .feather')
            else:
                raise FileNotFoundError('Данного файла не существует')
        except Exception as error:
            print(f"Произошла ошибка: {error}")

    file_input = args.input

    """Проверка для сохранения таблицы в другом формате"""

    if args.output is None:
        raise FileNotFoundError('Не указан путь сохранения таблицы в другом формате')

    file_output = args.output


    """Проверка формата"""

    if args.format is None:
        raise TypeError('Нет указан конечный формат')

    format_type = args.format

    """Чтение таблицы dataframe в формате .feather"""

    df = pd.read_feather(file_input)

    print('Таблица:')
    print(df)
    print()

    """Переформатирование и сохранение таблицы"""

    base_name = os.path.basename(file_input)
    base_name = os.path.splitext(base_name)[0]
    file_output = file_output + '\\' + base_name + '.' + format_type

    match format_type:
        case 'csv': df.to_csv(file_output, index=False, encoding='utf-8-sig')
        case 'xlsx': df.to_excel(file_output, index=False)
        case 'xml': df.to_xml(file_output, index=False)
        case 'json': df.to_json(file_output, force_ascii=False)
        case 'html': df.to_html(file_output, index=False)
        case 'sql': df_to_sql(df, file_output, base_name)
        case 'none': pass
        case _: raise ValueError('Недопустимый формат')

    print(f'Таблица сохранена по адресу {file_output}')