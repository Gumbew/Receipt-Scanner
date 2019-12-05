import configparser

from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient

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
