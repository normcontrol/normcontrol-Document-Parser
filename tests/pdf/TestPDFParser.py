import unittest
from src.pdf.PDFParser import PDFParser


class TestPDFParser(unittest.TestCase):
    path = 'documents\\Отчёт по практике для парсинга.pdf'
    pdf_parser = PDFParser(path=path)
    pdf_parser.get_all_elements(pdf_parser.lines, pdf_parser.line_spaces, pdf_parser.tables, pdf_parser.pictures)

    def test_parse_content(self):
        self.assertEqual(len(self.pdf_parser.tables), 8)
        self.assertEqual(len(self.pdf_parser.pictures), 12)
        self.assertEqual(self.pdf_parser.document.content[1].indent, 7.88)
        self.assertEqual(self.pdf_parser.document.content[1].font_name, ['TimesNewRomanPSMT'])
        self.assertEqual(self.pdf_parser.document.content[1].text_size, [14])
        self.assertEqual(self.pdf_parser.document.content[1].text, 'Введение ')
        self.assertEqual(self.pdf_parser.document.content[1].no_change_fontname, True)
        self.assertEqual(self.pdf_parser.document.content[1].no_change_text_size, True)
        self.assertEqual(self.pdf_parser.document.content[1].bbox, {1: (308.35, 783.20736, 368.62, 769)})
        self.assertEqual(self.pdf_parser.document.content[1].count_of_sp_sbl, 0)
        self.assertEqual(self.pdf_parser.document.content[1].last_sbl, ' ')
        self.assertEqual(self.pdf_parser.document.content[1].first_key, '')
        self.assertEqual(self.pdf_parser.document.content[1].bold, False)
        self.assertEqual(self.pdf_parser.document.content[1].italics, False)
        self.assertEqual(self.pdf_parser.document.content[1].uppercase, False)
        self.assertEqual(self.pdf_parser.document.content[1].lowercase, False)

        self.assertEqual(self.pdf_parser.document.content[23].indent, 1.89)
        self.assertEqual(set(self.pdf_parser.document.content[23].font_name),
                         {'TimesNewRomanPSMT', 'ArialMT', 'SymbolMT'})
        self.assertEqual(self.pdf_parser.document.content[23].text_size, [14])
        self.assertEqual(self.pdf_parser.document.content[23].text, '− жесткий диск: HDD 40 Гб в RAID 1. ')
        self.assertEqual(self.pdf_parser.document.content[23].no_change_fontname, False)
        self.assertEqual(self.pdf_parser.document.content[23].no_change_text_size, True)
        self.assertEqual(self.pdf_parser.document.content[23].bbox, {2: (138.5, 223.54736, 377.02, 210)})
        self.assertEqual(self.pdf_parser.document.content[23].count_of_sp_sbl, 2)
        self.assertEqual(self.pdf_parser.document.content[23].last_sbl, '.')
        self.assertEqual(self.pdf_parser.document.content[23].first_key, 'listLevel1')
        self.assertEqual(self.pdf_parser.document.content[23].bold, False)
        self.assertEqual(self.pdf_parser.document.content[23].italics, False)
        self.assertEqual(self.pdf_parser.document.content[23].uppercase, False)
        self.assertEqual(self.pdf_parser.document.content[23].lowercase, False)

        self.assertEqual(self.pdf_parser.document.content[33].indent, 1.25)
        self.assertEqual(set(self.pdf_parser.document.content[33].font_name),
                         {'SymbolMT', 'TimesNewRomanPSMT', 'ArialMT'})
        self.assertEqual(self.pdf_parser.document.content[33].text_size, [14])
        self.assertEqual(self.pdf_parser.document.content[33].text, '− Nginx: 1.21.6 + ssl_preread, image_filter, '
                                                                    'geoip, geoip2, brotli; ')
        self.assertEqual(self.pdf_parser.document.content[33].no_change_fontname, False)
        self.assertEqual(self.pdf_parser.document.content[33].no_change_text_size, True)
        self.assertEqual(self.pdf_parser.document.content[33].bbox, {3: (120.5, 184.42736, 515.41, 170)})
        self.assertEqual(self.pdf_parser.document.content[33].count_of_sp_sbl, 8)
        self.assertEqual(self.pdf_parser.document.content[33].last_sbl, ';')
        self.assertEqual(self.pdf_parser.document.content[33].first_key, 'listLevel1')
        self.assertEqual(self.pdf_parser.document.content[33].bold, False)
        self.assertEqual(self.pdf_parser.document.content[33].italics, False)
        self.assertEqual(self.pdf_parser.document.content[33].uppercase, False)
        self.assertEqual(self.pdf_parser.document.content[33].lowercase, False)

        self.assertEqual(self.pdf_parser.document.content[38].bbox, (125.9, 484.07, 548.05, 736.92))
        self.assertEqual(self.pdf_parser.document.content[38].width, 422.15)
        self.assertEqual(self.pdf_parser.document.content[38].height, 422.15)
        self.assertEqual(self.pdf_parser.document.content[38].page_number, 4)

        self.assertEqual(self.pdf_parser.document.content[65].bbox, (85.46399499999998, 81.2399999999999,
                                                                     552.9600149999998, 432.28999999999996))
        self.assertEqual(self.pdf_parser.document.content[65].page_bbox, (0, 0, 595.32, 841.92))
        self.assertEqual(self.pdf_parser.document.content[65].master_page_number, 7)

        self.assertEqual(self.pdf_parser.document.content[72].bbox, (90.45, 330.92, 558.2, 711.77))
        self.assertEqual(self.pdf_parser.document.content[72].width, 467.75000000000006)
        self.assertEqual(self.pdf_parser.document.content[72].height, 467.75000000000006)
        self.assertEqual(self.pdf_parser.document.content[72].page_number, 8)

    def test_parse_pictures(self):
        self.assertEqual(len(self.pdf_parser.pictures), 12)

        self.assertEqual(self.pdf_parser.pictures[1].bbox, (125.9, 484.07, 548.05, 736.92))
        self.assertEqual(self.pdf_parser.pictures[1].width, 422.15)
        self.assertEqual(self.pdf_parser.pictures[1].height, 422.15)
        self.assertEqual(self.pdf_parser.pictures[1].page_number, 4)

        self.assertEqual(self.pdf_parser.pictures[5].bbox, (212.8, 171.76, 424.55, 785.23))
        self.assertEqual(self.pdf_parser.pictures[5].width, 211.75)
        self.assertEqual(self.pdf_parser.pictures[5].height, 211.75)
        self.assertEqual(self.pdf_parser.pictures[5].page_number, 12)

        self.assertEqual(self.pdf_parser.pictures[9].bbox, (90.45, 515.33, 494.9, 736.9200000000001))
        self.assertEqual(self.pdf_parser.pictures[9].width, 404.45)
        self.assertEqual(self.pdf_parser.pictures[9].height, 404.45)
        self.assertEqual(self.pdf_parser.pictures[9].page_number, 17)

        self.assertEqual(self.pdf_parser.pictures[11].bbox, (118.42, 494.24, 518.87, 785.22))
        self.assertEqual(self.pdf_parser.pictures[11].width, 400.45)
        self.assertEqual(self.pdf_parser.pictures[11].height, 400.45)
        self.assertEqual(self.pdf_parser.pictures[11].page_number, 22)

    def test_parse_paragraphs(self):
        self.assertEqual(self.pdf_parser.document.content[17].indent, 1.25)
        self.assertEqual(self.pdf_parser.document.content[17].font_name, ['TimesNewRomanPSMT'])
        self.assertEqual(self.pdf_parser.document.content[17].text_size, [14])
        self.assertEqual(self.pdf_parser.document.content[17].text, 'Основной причиной этого стало то, что '
                                                                    'большинство пользователей MS Word никогда не '
                                                                    'пользовались функцией надстроек, а некоторые '
                                                                    'даже не знают, что это такое. Также оказалось, '
                                                                    'что разработанный интерфейс для пользователей не '
                                                                    'очень удобен и местами непонятен. Большим '
                                                                    'недостатком оказалась сложность установки '
                                                                    'сервиса на клиентский компьютер пользователями '
                                                                    'не имевших такой опыт. ')
        self.assertEqual(self.pdf_parser.document.content[17].no_change_fontname, True)
        self.assertEqual(self.pdf_parser.document.content[17].no_change_text_size, True)
        self.assertEqual(self.pdf_parser.document.content[17].bbox, {2: (85.104, 614.10736, 556.47, 479)})
        self.assertEqual(self.pdf_parser.document.content[17].count_of_sp_sbl, 7)
        self.assertEqual(self.pdf_parser.document.content[17].last_sbl, '.')
        self.assertEqual(self.pdf_parser.document.content[17].first_key, '')
        self.assertEqual(self.pdf_parser.document.content[17].bold, False)
        self.assertEqual(self.pdf_parser.document.content[17].italics, False)
        self.assertEqual(self.pdf_parser.document.content[17].uppercase, False)
        self.assertEqual(self.pdf_parser.document.content[17].lowercase, False)

        self.assertEqual(self.pdf_parser.document.content[55].indent, 1.25)
        self.assertEqual(set(self.pdf_parser.document.content[55].font_name),
                         {'SymbolMT', 'TimesNewRomanPSMT', 'ArialMT'})
        self.assertEqual(self.pdf_parser.document.content[55].text_size, [14])
        self.assertEqual(self.pdf_parser.document.content[55].text, '− обезличенные данные для обучения '
                                                                    'классификатора; ')
        self.assertEqual(self.pdf_parser.document.content[55].no_change_fontname, False)
        self.assertEqual(self.pdf_parser.document.content[55].no_change_text_size, True)
        self.assertEqual(self.pdf_parser.document.content[55].bbox, {6: (120.5, 540.5173599999999, 477.73, 526)})
        self.assertEqual(self.pdf_parser.document.content[55].count_of_sp_sbl, 1)
        self.assertEqual(self.pdf_parser.document.content[55].last_sbl, ';')
        self.assertEqual(self.pdf_parser.document.content[55].first_key, 'listLevel1')
        self.assertEqual(self.pdf_parser.document.content[55].bold, False)
        self.assertEqual(self.pdf_parser.document.content[55].italics, False)
        self.assertEqual(self.pdf_parser.document.content[55].uppercase, False)
        self.assertEqual(self.pdf_parser.document.content[55].lowercase, True)

        self.assertEqual(self.pdf_parser.document.content[77].indent, 1.25)
        self.assertEqual(set(self.pdf_parser.document.content[77].font_name),
                         {'TimesNewRomanPSMT', 'ArialMT'})
        self.assertEqual(self.pdf_parser.document.content[77].text_size, [14])
        self.assertEqual(self.pdf_parser.document.content[77].text,
                         '3 Модернизация сервиса автоматизированного нормоконтроля документов ')
        self.assertEqual(self.pdf_parser.document.content[77].no_change_fontname, False)
        self.assertEqual(self.pdf_parser.document.content[77].no_change_text_size, True)
        self.assertEqual(self.pdf_parser.document.content[77].bbox, {9: (85.104, 758.94736, 556.1242399999999, 721)})
        self.assertEqual(self.pdf_parser.document.content[77].count_of_sp_sbl, 0)
        self.assertEqual(self.pdf_parser.document.content[77].last_sbl, ' ')
        self.assertEqual(self.pdf_parser.document.content[77].first_key, 'TitleLevel1')
        self.assertEqual(self.pdf_parser.document.content[77].bold, False)
        self.assertEqual(self.pdf_parser.document.content[77].italics, False)
        self.assertEqual(self.pdf_parser.document.content[77].uppercase, False)
        self.assertEqual(self.pdf_parser.document.content[77].lowercase, False)

    def test_parse_tables(self):
        self.assertEqual(self.pdf_parser.tables[3].bbox, (85.10400000000003, 623.8600099999999,
                                                          552.9599900000001, 775.8960099999999))
        self.assertEqual(self.pdf_parser.tables[3].page_bbox, (0, 0, 595.32, 841.92))
        self.assertEqual(self.pdf_parser.tables[3].master_page_number, 17)

        self.assertEqual(self.pdf_parser.tables[5].bbox, (96.504, 346.729995, 541.5599899999999, 595.7500099999999))
        self.assertEqual(self.pdf_parser.tables[5].page_bbox, (0, 0, 595.32, 841.92))
        self.assertEqual(self.pdf_parser.tables[5].master_page_number, 19)

        self.assertEqual(self.pdf_parser.tables[7].bbox, (85.10400000000001, 82.31999999999994,
                                                          532.92002, 197.05999999999995))
        self.assertEqual(self.pdf_parser.tables[7].page_bbox, (0, 0, 595.32, 841.92))
        self.assertEqual(self.pdf_parser.tables[7].master_page_number, 23)
