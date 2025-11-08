# self-testing purposes
# simply gets a frame and applies the algorithm

import cv2 as cv
import numpy as np
import os

root = os.getcwd()

images_folder = os.path.join(root, "images")

img = cv.imread(os.path.join(images_folder, "frame8.png"))

gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

thresh = cv.GaussianBlur(gray_img, (5, 5), 0)

edged = cv.Canny(thresh, 0, 40)

final_mask_dilate = cv.dilate(edged, np.ones((15, 15), dtype=np.uint8))
final_mask = cv.erode(final_mask_dilate, np.ones((15, 15), dtype=np.uint8))
# flipped_mask = cv.bitwise_not(final_mask)

edged = cv.copyMakeBorder(
    final_mask, top=1, bottom=1, left=1, right=1, borderType=cv.BORDER_CONSTANT, value=1
)

structuring_element = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
final_edged = cv.morphologyEx(edged, cv.MORPH_OPEN, structuring_element)

contours, hierarchy = cv.findContours(edged.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

for cnt in contours:
    if cv.contourArea(cnt) < 10000 or cv.contourArea(cnt) > 1000000:
        continue
    cv.drawContours(img, cnt, -1, (255, 255, 0), 5)

    M = cv.moments(cnt)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    cv.circle(img, (cX, cY), 7, (255, 255, 255), -1)

    # x, y, w, h = cv.boundingRect(cnt)
    # cv.rectangle(img, (x, y), (x+w, y+h), (0, 255, 255), 5)
