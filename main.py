from receipt_scanner_ocr import ReceiptScannerOCR
from pprint import pprint

image_path = r"images\3.jpg"
receipt_dict = ReceiptScannerOCR.image_to_text(image_path, False)
pprint(receipt_dict)




