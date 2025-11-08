# self-testing purposes
# gets frames of video to individually analyze

import cv2 as cv
import os

root = os.getcwd()

images_folder = os.path.join(root, "images")

if os.system("cd " + images_folder + "> /dev/null 2>&1") != 0:
    os.system("mkdir images")

vid = cv.VideoCapture("../../../resources/test.mp4")

count, success = 0, True

while count < 30 and success:
    success, img = vid.read()
    if success:
        cv.imwrite(os.path.join(images_folder, f"frame{count}.png"), img)
        count += 1
