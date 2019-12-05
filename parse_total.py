import re


def parse_total(text):
    res = re.search(r'(\d+[.,]\d{1,2}|\d+)', text)
    return {'total': res.group(0), 'currency': 'UAH'}


def _test():
    print('Testing parse_datetime:')
    data = [
        ['СУМА\nПДВ А « 20005', '20005'],
        ['сума а,за\nПВА 28,085 8,72\nсУма ПДВ 8,72', '28,08'],
        ['ІД:\n\n10.50 ГРН', '10.50']
    ]

    for i in data:
        actual = parse_total(i[0])
        expected = i[1]

        if actual["total"] == expected:
            print(f' > {actual["total"]} - passed')
        else:
            print(f'FAIL: actual={actual} != expected={expected}')


if __name__ == "__main__":
    _test()
