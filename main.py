import cv2
import pytesseract
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
import configparser
import filters_and_binarisation

config = configparser.ConfigParser()
config.read('config.ini')


class ReceiptScannerApi:
    ENDPOINT = config['Azure']['ENDPOINT']
    training_key = config['Azure']['training_key']
    prediction_key = config['Azure']['prediction_key']
    prediction_resource_id = config['Azure']['prediction_resource_id']
    project_id = config['Azure']['project_id']
    publish_iteration_name = config['Azure']['publish_iteration_name']

    predictor = CustomVisionPredictionClient(prediction_key, endpoint=ENDPOINT)

    @staticmethod
    def get_prediction_results(image_path: str) -> list:
        with open(image_path, mode="rb") as test_data:
            return ReceiptScannerApi.predictor.detect_image(
                ReceiptScannerApi.project_id,
                ReceiptScannerApi.publish_iteration_name,
                test_data
            )

    @staticmethod
    def print_prediction_results(results: str) -> None:
        for prediction in results.predictions:
            print(
                "\t" + prediction.tag_name + ": {0:.2f}% bbox.left = {1:.2f}, bbox.top = {2:.2f}, bbox.width = {3:.2f}, bbox.height = {4:.2f}".format(
                    prediction.probability * 100, prediction.bounding_box.left, prediction.bounding_box.top,
                    prediction.bounding_box.width, prediction.bounding_box.height))


class ReceiptParser:

    @staticmethod
    def get_rectangle_properties(image_width, image_height, prediction):
        rectangle_properties = {}

        rectangle_width = prediction.bounding_box.width * image_width
        rectangle_height = prediction.bounding_box.height * image_height
        rectangle_properties['width'] = round(rectangle_width)
        rectangle_properties['height'] = round(rectangle_height)
        rectangle_properties['x1'] = round(prediction.bounding_box.left * image_width)
        rectangle_properties['y1'] = round(prediction.bounding_box.top * image_height)
        rectangle_properties['x2'] = round(rectangle_properties['x1'] + rectangle_width)
        rectangle_properties['y2'] = round(rectangle_properties['y1'] + rectangle_height)

        return rectangle_properties

    @staticmethod
    def draw_bounding_boxes(input_image_path, output_image_path, predictions):
        image = cv2.imread(input_image_path)
        height, width, channels = image.shape

        for prediction in predictions:
            rectangle_properties = ReceiptParser.get_rectangle_properties(width, height, prediction)
            cv2.rectangle(image, (rectangle_properties['x1'], rectangle_properties['y1']),
                          (rectangle_properties['x2'], rectangle_properties['y2']), (255, 0, 0), 2)
        cv2.imwrite(output_image_path, image)

    @staticmethod
    def draw_bounding_boxes_dict(input_image_path, output_image_path, predictions):
        image = cv2.imread(input_image_path)
        height, width, channels = image.shape
        for prediction in predictions:
            rectangle_width = predictions[prediction].bounding_box.width * width
            rectangle_height = predictions[prediction].bounding_box.height * height
            x1 = round(predictions[prediction].bounding_box.left * width)
            y1 = round(predictions[prediction].bounding_box.top * height)
            x2 = round(x1 + rectangle_width)
            y2 = round(y1 + rectangle_height)
            cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.imwrite(output_image_path, image)

    @staticmethod
    def get_top_predictions(predictions):
        prediction_tags = {prediction.tag_name for prediction in predictions}
        top_predictions = {}
        for prediction_tag in prediction_tags:
            for prediction in predictions:
                if prediction.tag_name == prediction_tag:
                    if prediction_tag not in top_predictions:
                        top_predictions[prediction_tag] = prediction
                    else:
                        if top_predictions[prediction_tag].probability < prediction.probability:
                            top_predictions[prediction_tag] = prediction
        return top_predictions

    @staticmethod
    def crop_image_by_predictions(image_path, predictions):
        image = cv2.imread(image_path)
        height, width, channels = image.shape
        top_predictions = ReceiptParser.get_top_predictions(predictions)
        for prediction in top_predictions:
            props = ReceiptParser.get_rectangle_properties(width, height, top_predictions[prediction])
            image_name = image_path.split('.')[0]
            image_ext = image_path.split('.')[1]
            cv2.imwrite(f'{image_name}{top_predictions[prediction].tag_name}.{image_ext}',
                        image[props['y1']:props['y1'] + props['height'], props['x1']:props['x1'] + props['width']])


image_path = "images\999.jpg"
output_image_path = "911_boxes_all.jpg"
output_image_path_ = "911_boxes.jpg"
result = ReceiptScannerApi.get_prediction_results(image_path)
ReceiptScannerApi.print_prediction_results(result)
ReceiptParser.draw_bounding_boxes(image_path, output_image_path, result.predictions)
top_predictions = ReceiptParser.get_top_predictions(result.predictions)
print(top_predictions['goods'].probability)
ReceiptParser.draw_bounding_boxes_dict(image_path, output_image_path_, top_predictions)
ReceiptParser.crop_image_by_predictions(image_path, result.predictions)

filters_and_binarisation.apply_filters('images\999date.jpg', 'images\999date_f.jpg')
print(pytesseract.image_to_string(cv2.imread('images\999date.jpg'), lang='ukr'))
print('**********')
receipt_date = pytesseract.image_to_string(cv2.imread('images\999date_f.jpg'), lang='ukr')

# date_time_obj = datetime.datetime.strptime(receipt_date, '%d.%m.%Y %H:%M')
# print(date_time_obj.date())
