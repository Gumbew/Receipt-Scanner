import re
import pprint


def parse_header(header):
    print(' -> info: parsing header:\n -{}\n\n'.format(header))
    header = re.sub('\n{2,}', '\n', header)
    lines = header.split('\n')
    llc = _pop_llc(lines)
    shop_name = _pop_shop_name(lines)
    tax_number = _pop_tax_number(lines)
    return llc, shop_name, tax_number


def _pop_tax_number(lines):
    for line in lines:
        match = re.search(r".*[ПІ]Н\s+(\d{9,}).*", line)
        if match != None:
            lines.remove(line)
            return match.group(1)
    return None


def _pop_shop_name(lines):
    for line in lines:
        match = re.search(r'.*[МмЧч][Аа][Гг][Аа][Зз][Ии][Нн]\s+(.+)', line)
        if match != None:
            lines.remove(line)
            return re.sub(r'["\']', '', match.group(1))

        match = re.search(r"[МмН][Аа][Гг][Аа][Зз][Ии][Нн]", line)
        if match != None:
            print(f' -> info: found shop line without the name: {line}')
            lines.remove(line)
    return None


def _pop_llc(lines):
    for line in lines:
        match = re.search(r'.*([ТтГ][Оo0][Вв68]|[ТтГ][Зз3][Оо0][Вв68].[ТтГ][Вв86][Кк])\s+(.+)', line)
        if match != None:
            lines.remove(line)
            return re.sub(r'["\']', '', match.group(2))
    return None


def _test():
    headers = [
        'ТОВ "Ф0331-РУД"\nмагазин TEST СІЛЬПО"\n\nМ. Київ\nв. Миколи Йаврухіна, БУЧІ\nМу ПН 322949218139',
        'МАГАЗИН "ЕКО МАРКЕТ"\nІВАНО- ФРАНКІВСЬК ОБЛ., ДОЛИНСЬКИЙ Р-Н\n\nМ.ДОЛИНА, ПР. НЕЗАЛЕЖНОСТІ, ЗА\nФН 3000340474 ІД 35495114\n\nЗН ТБ1001002160 ІН 354951103189\n\nгло 11 оновив',
        '«ТОВ "Фоззі-Фуд"\n- 2 с Магазин "Сільпо"\n1.Київ, вуп. Дніпровська наберезна, 33\n- - . ПН 322949218139\nтт .',
        'Гз0ВОТ6К "Львівхолод"\nЧагазин "Рукавичка"\nЛьвівська обл.,\nн.Львів, м.Чайковського, 31\nПН 015536813049.\nЗ СП802400581  9н 3000487744\nКлепач Нарта Каса 03',
        'ТОВ "атБб-Нна кет"\n, НАГАЗИН ПРОДУКТИ (б\nН.ХЕРСОН, ВУЛ.ЄТРІТЕНСЬКА, 7\n1. (0552342 -90- 42, (0552)42-9)- 43\nПН. 3048 872 104175\n\nЧНОооТтаб9А мір Аллан',
        'МАГАЗИН "ЕКО МАРКЕТ"\nТВАНО-ФРАНКІВСЬКА ОБ/.» ДОЛИНСЬКИЙ РАН\n\nМ.ДОЛИНА. ПР. НЕЗАИЕЖНОСТІ, ЗА\n9Н 3000340474 І 35495114\nН Т51001002158 ПН 354951103189\n\nзе" ча поту пита ше 00 умо',
        'ТОВ "АЛЬЯНС НАРКЕТ"\nМагазин\nм.Львів, Галицький р-н,\nпл. Міцкевича В., буд. 5\nПН 383161126504',
        'ТОВ "АЛЬЯНС МАРКЕТ"\nМагазин\nн.Львів, Галицький р-н,\nпл Міцкевича й,, буд. 5\nПН 383167796584\n\nЦарллап "Об'
    ]

    for header in headers:
        print('********************')
        print(header)
        print('--------------------')
        parse_header(header)
        print('--------------------')
        print('\n\n')


if __name__ == "__main__":
    _test()
