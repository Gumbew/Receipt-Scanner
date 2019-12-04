import cv2


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

        if len(image.shape) == 3:
            height, width, _ = image.shape
        else:
            height, width = image.shape

        for prediction in predictions:
            rectangle_properties = ReceiptParser.get_rectangle_properties(width, height, prediction)
            cv2.rectangle(image, (rectangle_properties['x1'], rectangle_properties['y1']),
                          (rectangle_properties['x2'], rectangle_properties['y2']), (255, 0, 0), 2)
        cv2.imwrite(output_image_path, image)

    @staticmethod
    def draw_bounding_boxes_dict(input_image_path, output_image_path, predictions):
        image = cv2.imread(input_image_path)

        if len(image.shape) == 3:
            height, width, _ = image.shape
        else:
            height, width = image.shape

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
    def crop_image_by_prediction(image, prediction_name):

        if len(image.shape) == 3:
            height, width, _ = image.shape
        else:
            height, width = image.shape

        props = ReceiptParser.get_rectangle_properties(width, height, prediction_name)

        return image[props['y1']:props['y1'] + props['height'], props['x1']:props['x1'] + props['width']]
