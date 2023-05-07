from src.classes.Table import Table
from src.classes.TableRow import TableRow
from src.classes.TableCell import TableCell
from dacite import from_dict

def convert_to_list(list_data: dict):
    """Converts the list data into a dictionary for further initialization of the object.

    Keyword arguments:
        list_data: dict - dictionary with list data.
    ----------
    Конвертирует данные списка в словарь для дальнейшей инициализации объекта.

    Аргументы:
        list_data: dict - словарь с данными списка.
    """
    converted_data = {}
    data_keys = list(list_data.keys())
    for element in data_keys:
        converted_data_key = {}
        match element:
            case 'name':
                converted_data_key['_list_name'] = list_data[element]
            case 'level':
                converted_data_key['_list_level'] = list_data[element]
            case 'start-value':
                converted_data_key['_list_start_value'] = list_data[element]
            case 'bullet-char':
                converted_data_key['_list_style_char'] = list_data[element]
            case 'style-name':
                converted_data_key['_list_style_name'] = list_data[element]
        converted_data.update(converted_data_key)
    return converted_data

def convert_to_table(table_data: dict):
    """Converts the table data into a dictionary for further initialization of the object.

    Keyword arguments:
        table_data: dict - table style data.
    ----------
    Конвертирует данные таблицы в словарь для дальнейшей инициализации объекта.

    Аргументы:
        table_data: dict - данные стиля таблицы.
    """
    converted_data = {}
    data_keys = list(table_data.keys())
    for element in data_keys:
        converted_data_key = {}
        match element:
            case 'name':
                converted_data_key['_table_name'] = table_data[element]
            case 'family':
                converted_data_key['_table_family'] = table_data[element]
            case 'master-page-name':
                converted_data_key['_table_master_page_name'] = table_data[element]
            case 'width':
                converted_data_key['_table_properties_width'] = float(table_data[element].split('i')[0])
            case 'margin-left':
                converted_data_key['_table_properties_margin_left'] = float(table_data[element].split('i')[0])
            case 'align':
                converted_data_key['_table_properties_align'] = table_data[element]
        converted_data.update(converted_data_key)
    return converted_data

def get_tables_objects(tables_data: dict):
    """Constructs a list of table structural parts from relevant dictionaries.

    Keyword arguments:
        tables_data: dict - dictionary with table data.
    ----------
    Создает список структурных частей таблицы из соответствующих словарей.

    Аргументы:
        tables_data: dict - словарь с данными таблицы.
    """
    table_objs = []
    for cur_style in tables_data:
        if cur_style.count('Row') > 0:
            table_objs.append(from_dict(data_class=TableRow,
                                        data=convert_to_table_row(tables_data[cur_style])))
        elif cur_style.count('Cell') > 0:
            table_objs.append(from_dict(data_class=TableCell,
                                        data=convert_to_table_cell(tables_data[cur_style])))
        else:
            table_objs.append(from_dict(data_class=Table,
                                        data=convert_to_table(tables_data[cur_style])))
    return table_objs

def convert_to_table_column(column_data: dict):
    """Converts the table column data into a dictionary for further initialization of the object.

    Keyword arguments:
        column_data: dict - dictionary with table column data.
    ----------
    Конвертирует данные столбца таблицы в словарь для дальнейшей инициализации объекта.

    Аргументы:
        column_data: dict - словарь с данными столбца таблицы.
    """
    converted_data = {}
    data_keys = list(column_data.keys())
    for element in data_keys:
        converted_data_key = {}
        match element:
            case 'name':
                converted_data_key['_column_name'] = column_data[element]
            case 'family':
                converted_data_key['_column_family'] = column_data[element]
            case 'column-width':
                converted_data_key['_column_properties_column_width'] = float(column_data[element].split('i')[0])
            case 'use-optimal-column-width':
                converted_data_key['_column_properties_use_optimal_column_width'] = column_data[element] == 'true'
        converted_data.update(converted_data_key)
    return converted_data

def convert_to_table_row(row_data: dict):
    """Converts the table row data into a dictionary for further initialization of the object.

    Keyword arguments:
        row_data: dict - dictionary with table row data.
    ----------
    Конвертирует данные строки таблицы в словарь для дальнейшей инициализации объекта.

    Аргументы:
        row_data: dict - словарь с данными строки таблицы.
    """
    converted_data = {}
    data_keys = list(row_data.keys())
    for element in data_keys:
        converted_data_key = {}
        match element:
            case 'name':
                converted_data_key['_row_name'] = row_data[element]
            case 'family':
                converted_data_key['_row_family'] = row_data[element]
            case 'min-row-height':
                converted_data_key['_row_properties_min_row_height'] = float(row_data[element].split('i')[0])
            case 'use-optimal-row-height':
                converted_data_key['_row_properties_use_optimal_row_height'] = row_data[element] == 'true'
        converted_data.update(converted_data_key)
    return converted_data

def convert_to_table_cell(cell_data: dict):
    """Converts the table cell data into a dictionary for further initialization of the object.

    Keyword arguments:
        cell_data: dict - dictionary with table cell data.
    ----------
    Конвертирует данные ячейки таблицы в словарь для дальнейшей инициализации объекта.

    Аргументы:
        cell_data: dict - словарь с данными столбца таблицы.
    """
    converted_data = {}
    data_keys = list(cell_data.keys())
    for element in data_keys:
        converted_data_key = {}
        match element:
            case 'name':
                converted_data_key['_cell_name'] = cell_data[element]
            case 'family':
                converted_data_key['_cell_family'] = cell_data[element]
            case 'border':
                converted_data_key['_cell_properties_border'] = float(cell_data[element].split('i')[0])
            case 'writing-mode':
                converted_data_key['_cell_properties_writing_mode'] = cell_data[element]
            case 'padding-top':
                converted_data_key['_cell_properties_padding_top'] = float(cell_data[element].split('i')[0])
            case 'padding-left':
                converted_data_key['_cell_properties_padding_left'] = float(cell_data[element].split('i')[0])
            case 'padding-bottom':
                converted_data_key['_cell_properties_padding_right'] = float(cell_data[element].split('i')[0])
            case 'padding-right':
                converted_data_key['_cell_properties_padding_bottom'] = float(cell_data[element].split('i')[0])
        converted_data.update(converted_data_key)
    return converted_data