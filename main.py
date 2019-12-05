#!/usr/bin/python3

from ocr import ReceiptScannerOCR
from pprint import pprint

image_path = r"images\3.jpg"
receipt_dict = ReceiptScannerOCR.image_to_text(image_path, True)
pprint(receipt_dict)

