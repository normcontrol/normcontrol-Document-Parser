from src.classes.Table import Table
from src.classes.TableColumn import TableColumn
from src.classes.TableRow import TableRow
from src.classes.TableCell import TableCell
from dacite import from_dict

def convert_to_list(list_name: str, list_data: dict):
    """Converts the list data into a dictionary for further initialization of the object.

    Keyword arguments:
        list_name: str - name of the list style;
        list_data: dict - list style data.
    ----------
    Конвертирует данные списка в словарь для дальнейшей инициализации объекта.

    Аргументы:
        list_name: str - название стиля списка;
        list_data: dict - данные стиля списка.
    """
    converted_data = {}
    data_keys = list(list_data.keys())
    if 'number' in data_keys[0]:
        converted_data.update({'_list_type': 'numbered'})
    else:
        converted_data.update({'_list_type': 'bulleted'})
    converted_data.update({'_list_name': list_name})
    for element in data_keys:
        cur_element = element.split('/')
        match cur_element[1]:
            case 'level':
                converted_data.update({'_list_level': list_data[element]})
            case 'start-value':
                converted_data.update({'_list_start_value': list_data[element]})
            case 'bullet-char':
                converted_data.update({'_list_style_char': list_data[element]})
            case 'style-name':
                converted_data.update({'_list_style_name': list_data[element]})
    return converted_data

def convert_to_table(table_name: str, table_data: dict):
    """Converts the table data into a dictionary for further initialization of the object.

    Keyword arguments:
        table_name: str - name of the table style;
        table_data: dict - table style data.
    ----------
    Конвертирует данные таблицы в словарь для дальнейшей инициализации объекта.

    Аргументы:
        table_name: str - название стиля таблицы;
        table_data: dict - данные стиля таблицы.
    """
    converted_data = {}
    data_keys = list(table_data.keys())
    converted_data.update({'_table_name': table_name})
    for element in data_keys:
        cur_element = element.split('/')
        match cur_element[1]:
            case 'family':
                converted_data.update({'_table_family': table_data[element]})
            case 'master-page-name':
                converted_data.update({'_table_master_page_name': table_data[element]})
            case 'width':
                converted_data.update({'_table_properties_width': float(table_data[element].split('i')[0])})
            case 'margin-left':
                converted_data.update({'_table_properties_margin_left': float(table_data[element].split('i')[0])})
            case 'align':
                converted_data.update({'_table_properties_align': table_data[element]})
    return converted_data

def get_tables_objects(tables_data: dict):
    """Returns a list of initialized table objects from the dictionary with prepared data.

    Keyword arguments:
        tables_data: dict - table cell style data.
    ----------
    Возвращает список инициализированных табличных объектов из словаря с подготовленными данными.

    Аргументы:
        tables_data: dict - данные стиля ячейки таблицы.
    """
    table_objs = []
    for cur_style in tables_data:
        if cur_style.count('Column') > 0:
            table_objs.append(from_dict(data_class=TableColumn,
                                        data=convert_to_table_column(cur_style, tables_data[cur_style])))
        elif cur_style.count('Row') > 0:
            table_objs.append(from_dict(data_class=TableRow,
                                        data=convert_to_table_row(cur_style, tables_data[cur_style])))
        elif cur_style.count('Cell') > 0:
            table_objs.append(from_dict(data_class=TableCell,
                                        data=convert_to_table_cell(cur_style, tables_data[cur_style])))
        else:
            table_objs.append(from_dict(data_class=Table,
                                        data=convert_to_table(cur_style, tables_data[cur_style])))
    return table_objs

def convert_to_table_column(column_name: str, column_data: dict):
    """Converts the table column data into a dictionary for further initialization of the object.

    Keyword arguments:
        column_name: str - name of the table column style;
        column_data: dict - table column style data.
    ----------
    Конвертирует данные столбца таблицы в словарь для дальнейшей инициализации объекта.

    Аргументы:
        column_name: str - название стиля столбца таблицы;
        column_data: dict - данные стиля столбца таблицы.
    """
    converted_data = {}
    data_keys = list(column_data.keys())
    converted_data.update({'_column_name': column_name})
    for element in data_keys:
        cur_element = element.split('/')
        match cur_element[1]:
            case 'family':
                converted_data.update({'_column_family': column_data[element]})
            case 'column-width':
                converted_data.update({'_column_properties_column_width': float(column_data[element].split('i')[0])})
            case 'use-optimal-column-width':
                converted_data.update({'_column_properties_use_optimal_column_width': column_data[element] == 'true'})
    return converted_data

def convert_to_table_row(row_name: str, row_data: dict):
    """Converts the table row data into a dictionary for further initialization of the object.

    Keyword arguments:
        row_name: str - name of the table row style;
        row_data: dict - table row style data.
    ----------
    Конвертирует данные строки таблицы в словарь для дальнейшей инициализации объекта.

    Аргументы:
        row_name: str - название стиля строки таблицы;
        row_data: dict - данные стиля строки таблицы.
    """
    converted_data = {}
    data_keys = list(row_data.keys())
    converted_data.update({'_row_name': row_name})
    for element in data_keys:
        cur_element = element.split('/')
        match cur_element[1]:
            case 'family':
                converted_data.update({'_row_family': row_data[element]})
            case 'min-row-height':
                converted_data.update({'_row_properties_min_row_height': float(row_data[element].split('i')[0])})
            case 'use-optimal-row-height':
                converted_data.update({'_row_properties_use_optimal_row_height': row_data[element] == 'true'})
    return converted_data

def convert_to_table_cell(cell_name: str, cell_data: dict):
    """Converts the table cell data into a dictionary for further initialization of the object.

    Keyword arguments:
        cell_name: str - name of the table cell style;
        cell_data: dict - table cell style data.
    ----------
    Конвертирует данные ячейки таблицы в словарь для дальнейшей инициализации объекта.

    Аргументы:
        cell_name: str - название стиля ячейки таблицы;
        cell_data: dict - данные стиля ячейки таблицы.
    """
    converted_data = {}
    data_keys = list(cell_data.keys())
    converted_data.update({'_cell_name': cell_name})
    for element in data_keys:
        cur_element = element.split('/')
        match cur_element[1]:
            case 'family':
                converted_data.update({'_cell_family': cell_data[element]})
            case 'border':
                converted_data.update({'_cell_properties_border': float(cell_data[element].split('i')[0])})
            case 'writing-mode':
                converted_data.update({'_cell_properties_writing_mode': cell_data[element]})
            case 'padding-top':
                converted_data.update({'_cell_properties_padding_top': float(cell_data[element].split('i')[0])})
            case 'padding-left':
                converted_data.update({'_cell_properties_padding_left': float(cell_data[element].split('i')[0])})
            case 'padding-bottom':
                converted_data.update({'_cell_properties_padding_right': float(cell_data[element].split('i')[0])})
            case 'padding-right':
                converted_data.update({'_cell_properties_padding_bottom': float(cell_data[element].split('i')[0])})
    return converted_data