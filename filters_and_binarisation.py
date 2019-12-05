import cv2


def apply_filters(image):
    if len(image.shape) == 3:
        height, width, _ = image.shape
    else:
        height, width = image.shape

    if height and width <= 1500:
        image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Denoising
    img_gray = cv2.fastNlMeansDenoising(img_gray, None, 10, 7, 21)

    # Binarization
    gaus = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 71, 11)
    return gaus
