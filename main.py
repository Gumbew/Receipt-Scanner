#!/usr/bin/python3

from ocr import ReceiptScannerOCR
from parse_header import parse_header
from parse_total import parse_total
from parse_datetime import parse_datetime

from pprint import pprint
import sys
import json

#image_path = r"images/2.jpg"
image_path = sys.argv[1]

receipt_dict = ReceiptScannerOCR.image_to_text(image_path, True)

total = parse_total(receipt_dict['total'])
llc, shop_name, tax_number = parse_header(receipt_dict['header'])
datetime = parse_datetime(receipt_dict['date'])

result = {
        'llc': llc,
        'shopName': shop_name,
        'taxNumber': tax_number,
        'total': {
            'value': total,
            'currency': 'UAH'
        },
        'datetime': datetime
}

print(json.dumps(result, indent=4, ensure_ascii=False))
