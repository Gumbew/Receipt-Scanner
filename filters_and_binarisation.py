import cv2

# # # from skimage.filters import threshold_otsu, threshold_local
# # image_path = '91.jpg'
# # image = cv2.imread(image_path,0)
# # # global_thresh = threshold_otsu(image)
# # # binary_global = image > global_thresh
# # #
# # # block_size = 3
# # # binary_adaptive = threshold_local(image, block_size, offset=1)
# # # cv2.imwrite('91_ba.jpg', binary_adaptive)
# # # cv2.imwrite('91_bg.jpg', binary_global)
# #
# # histogram = cv2.calcHist([image], [0], None, [256], [0, 256])
# # ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)
# # channels = cv2.split(ycrcb)
# # cv2.equalizeHist(channels[0], channels[0])
# # cv2.merge(channels, ycrcb)
# # cv2.cvtColor(ycrcb, cv2.COLOR_YCR_CB2BGR, image)
# # cv2.imwrite('images\9_eq.jpeg', image)
# #
# # img = cv2.imread('images\9_eq.jpeg')
# # img = cv2.imread(image_path)
#
#
# # img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
#
# # img = cv2.blur(img,(5,5))
# # img = cv2.GaussianBlur(img, (5, 5), 0)
#
# # img = cv2.bilateralFilter(img,9,75,75)
#
#
# cv2.imwrite('9_median_39_18_eq_nois_b_croped.jpeg', gaus)
# print(pytesseract.image_to_string(gaus, lang='ukr'))

def apply_filters(image_path, output_image_path):
    image = cv2.imread(image_path)

    # equalization
    # ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)
    # channels = cv2.split(ycrcb)
    # cv2.equalizeHist(channels[0], channels[0])
    # cv2.merge(channels, ycrcb)
    # cv2.cvtColor(ycrcb, cv2.COLOR_YCR_CB2BGR, image)
    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Denoising
    img_gray = cv2.fastNlMeansDenoising(img_gray, None, 10, 7, 21)

    # Binarization
    #gaus = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 91, 9)
    cv2.imwrite(output_image_path, img_gray)
