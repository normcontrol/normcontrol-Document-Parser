from src.classes.Table import Table
from src.classes.TableColumn import TableColumn
from src.classes.TableRow import TableRow
from src.classes.TableCell import TableCell
from dacite import from_dict

def convert_to_list(list_name: str, list_data: dict):
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