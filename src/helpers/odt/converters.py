from src.classes.Image import Image
from src.classes.Table import Table
from src.classes.TableRow import TableRow
from src.classes.TableCell import TableCell
from dacite import from_dict

from src.helpers.enums.AlignmentEnum import AlignmentEnum


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
    list_type = {}
    if 'bullet-char' in data_keys:
        list_type = {'_type': 'bulleted'}
    else: list_type = {'type': 'numbered'}
    converted_data.update(list_type)
    for element in data_keys:
        converted_data_key = {}
        match element:
            case 'name':
                converted_data_key['_name'] = list_data[element]
            case 'level':
                converted_data_key['_level'] = list_data[element]
            case 'start-value':
                converted_data_key['_start_value'] = list_data[element]
            case 'bullet-char':
                converted_data_key['_style_char'] = list_data[element]
            case 'style-name':
                converted_data_key['_style_name'] = list_data[element]
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

def convert_to_image(image_data: dict):
    """Converts the image data into a dictionary for further initialization of the object.

    Keyword arguments:
        image_data: dict - dictionary with image data.
    ----------
    Конвертирует данные изображения в словарь для дальнейшей инициализации объекта.

    Аргументы:
        image_data: dict - словарь с данными изображения.
    """
    converted_data = {}
    data_keys = list(image_data.keys())
    for element in data_keys:
        converted_data_key = {}
        match element:
            case 'href':
                converted_data_key['_href'] = image_data[element]
            case 'type':
                converted_data_key['_type'] = image_data[element]
            case 'show':
                converted_data_key['_show'] = image_data[element]
            case 'actuate':
                converted_data_key['_actuate'] = image_data[element]
        converted_data.update(converted_data_key)
    return converted_data

def convert_to_frame(frame_data: dict, image_data: Image):
    """Converts the frame data into a dictionary for further initialization of the object.

    Keyword arguments:
        frame_data: dict - dictionary with frame data;
        image_data: dict - dictionary with image data.
    ----------
    Конвертирует данные фрейма в словарь для дальнейшей инициализации объекта.

    Аргументы:
        frame_data: dict - словарь с данными фрейма;
        image_data: dict - словарь с данными изображения.
    """
    converted_data = {}
    converted_data_key = {}
    data_keys = list(frame_data.keys())
    for element in data_keys:
        converted_data_key = {}
        match element:
            case 'style-name':
                converted_data_key['_style_name'] = frame_data[element]
            case 'anchor-type':
                converted_data_key['_anchor_type'] = frame_data[element]
            case 'width':
                converted_data_key['_width'] = float(frame_data[element].split('i')[0])
            case 'height':
                converted_data_key['_height'] = float(frame_data[element].split('i')[0])
            case 'rel-width':
                converted_data_key['_rel_width'] = frame_data[element]
            case 'rel-height':
                converted_data_key['_rel_height'] = frame_data[element]
            case 'page-number':
                converted_data_key['_page_number'] = int(frame_data[element])
            case _:
                converted_data_key['_bbox'] = (float(frame_data['x'].split('i')[0]),
                                               float(frame_data['height'].split('i')[0]) * 138.9,
                                               float(frame_data['width'].split('i')[0]) * 138.9,
                                               float(frame_data['y'].split('i')[0]))
                converted_data_key['_image'] = image_data
        converted_data.update(converted_data_key)
    return converted_data

def convert_to_paragraph(par_props):
    converted_data = {}
    converted_data_key = {}
    for key in par_props.keys():
        converted_data_key = {}
        match key:
            case 'text-indent':
                converted_data_key['_indent'] = float(par_props[key].split('i')[0]) * 138.9
            case 'line-height':
                converted_data_key['_line_spacing'] = float(par_props[key].split('%')[0]) / 107
            # case 'text-align':
            #     if par_props[key] == 'start':
            #         converted_data_key['_alignment'] = AlignmentEnum.LEFT
            #     elif par_props[key] == 'center':
            #         converted_data_key['_alignment'] = AlignmentEnum.CENTER
            #     elif par_props[key] == 'justify':
            #         converted_data_key['_alignment'] = AlignmentEnum.JUSTIFY
            #     else:
            #         converted_data_key['_alignment'] = AlignmentEnum.RIGHT
            case 'margin-right':
                converted_data_key['_mrgrg'] = float(par_props[key].split('i')[0]) * 138.9
            case 'margin-top':
                converted_data_key['_mrgtop'] = float(par_props[key].split('i')[0]) * 138.9
            case 'margin-left':
                converted_data_key['_mrglf'] = float(par_props[key].split('i')[0]) * 138.9
            case 'margin-bottom':
                converted_data_key['_mrgbtm'] = float(par_props[key].split('i')[0]) * 138.9
            case 'keep-together':
                keep_together = False
                if par_props[key] == 'true':
                    keep_together = True
                converted_data_key['_keep_lines_together'] = keep_together
            case 'keep-with-next':
                keep_with_next = False
                if par_props[key] == 'true':
                    keep_with_next = True
                converted_data_key['_keep_with_next'] = keep_with_next
            case 'font-name':
                converted_data_key['_font_name'] = par_props[key]
            case 'text':
                converted_data_key['_text'] = par_props[key]
            case 'font-size':
                if isinstance(par_props[key], int):
                    converted_data_key['_text_size'] = float(par_props[key])
                else:
                    converted_data_key['_text_size'] = float(par_props[key][:2])
            # case '_count_of_sp_sbl':
            # case '_count_sbl':
            # case '_lowercase':
            # case '_uppercase':
            # case '_last_sbl':
            # case 'first-key':
            case 'font-weight':
                current_weight = True
                if par_props[key] == 'normal':
                    current_weight = False
                converted_data_key['_bold'] = current_weight
            case 'font-style':
                current_style = True
                if par_props[key] == 'normal':
                    current_style = False
                converted_data_key['_italics'] = current_style
            case 'text-underline-mode':
                current_underline = True
                if par_props[key] == 'false':
                    current_underline = False
                converted_data_key['_underlining'] = current_underline
            case 'text-position':
                current_position = par_props[key].split(' ')[0]
                if 'super' in current_position:
                    converted_data_key['_sub_text'] = False
                    converted_data_key['_super_text'] = True
                elif 'sub' in current_position:
                    converted_data_key['_sub_text'] = True
                    converted_data_key['_super_text'] = False
                else:
                    converted_data_key['_sub_text'] = False
                    converted_data_key['_super_text'] = False
            case 'color':
                converted_data_key['_color_text'] = par_props[key]
        converted_data.update(converted_data_key)
    return converted_data