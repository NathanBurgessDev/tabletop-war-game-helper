import cv2 as cv
import numpy as np


img = cv.imread("Contours/IMG_3139.jpg")

lower = (0, 200, 200)
upper = (100, 255, 255)
grayFrame = cv.inRange(img, lower, upper)


blurFrame = cv.GaussianBlur(grayFrame, (17, 17), 0)


thresh = cv.threshold(blurFrame, 60, 255, cv.THRESH_BINARY)[1]


cv.imshow("circles",thresh)

cv.waitKey(0)

# Min enclosing circle