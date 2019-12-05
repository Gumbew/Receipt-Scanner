# -*- encoding: utf-8 -*-
from recognizers_date_time import recognize_datetime, Culture
import re


def parse_datetime(datetime_string):
    print(' -> info: parsing datetime: {}\n\n'.format(datetime_string))
    datetime_string = _remove_trash(datetime_string)
    results = recognize_datetime(datetime_string, Culture.English)
    if len(results) == 0:
        return None

    value = results[0].resolution['values'][0]
    if value['type'] == 'daterange':
        return None
    else:
        return value['timex']

def _remove_trash(datetime_string):
    trim_trash_in_front = re.sub(r'(^.+?)(\d{2})', '\g<2>', datetime_string)
    remove_new_line = str.replace(trim_trash_in_front, '\n', ' ')
    remove_tab = str.replace(remove_new_line, '\t', ' ')
    remove_r = str.replace(remove_tab, '\r', ' ')
    replace_b_to_8 = str.replace(remove_r, 'B', '8')
    replace_b_to_8 = str.replace(replace_b_to_8, 'В', '8')
    res = replace_b_to_8
    return res


def _test():
    print('Testing parse_datetime:')
    data = [
        ['17-03-2015 16:04:22', '2015-03-17T16:04:22'],
        ['23/11/19 14:12', '2019-11-23T14:12'],
        ['29.11.2019', '2019-11-29'],
        ['22-01-2013 19:03:45', '2013-01-22T19:03:45'],
        ['11.11.2019 16:17', '2019-11-11T16:17'],
        ['22.12.2016 12:27', '2016-12-22T12:27'],
        ['30-11-19 10:43', '2019-11-30T10:43'],
        ['1.07.2017 11:46', '2017-07-01T11:46'],
        ['20/11/2019 19:36:12', '2019-11-20T19:36:12'],
        ['| 23/11/19 14:12 4', '2019-11-23T14:12']
    ]

    for i in range(len(data)):
        actual = parse_datetime(data[i][0])
        expected = data[i][1]

        if actual == expected:
            print(' > {} - passed ({} -> {})'.format(i, data[i][0], data[i][1]))
        else:
            print('FAIL: actual={} != expected={}'.format(actual, expected))


if __name__ == "__main__":
    _test()
