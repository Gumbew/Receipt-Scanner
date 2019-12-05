#!/usr/bin/python3

from ocr import ReceiptScannerOCR
from parse_header import parse_header
from pprint import pprint
import sys

#image_path = r"images/2.jpg"
image_path = sys.argv[1]

receipt_dict = ReceiptScannerOCR.image_to_text(image_path, True)
pprint(receipt_dict['header'])
