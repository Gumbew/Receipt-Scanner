import cv2
import pytesseract


import filters_and_binarisation

from receipt_parser import ReceiptParser
from api import ReceiptScannerApi


class ReceiptScannerOCR:
    @staticmethod
    def image_to_text(image_path, filters=False):
        receipt_dict = {}
        image = cv2.imread(image_path)

        if filters:
            image = filters_and_binarisation.apply_filters(image)

        all_predictions = ReceiptScannerApi.get_prediction_results(image_path).predictions
        top_predictions = ReceiptParser.get_top_predictions(all_predictions)
        prediction_tags = {prediction.tag_name for prediction in all_predictions}

        for tag in prediction_tags:
            cropped_image = ReceiptParser.crop_image_by_prediction(image, top_predictions[tag])
            text = pytesseract.image_to_string(cropped_image, lang='ukr')
            receipt_dict[tag] = text
        return receipt_dict
