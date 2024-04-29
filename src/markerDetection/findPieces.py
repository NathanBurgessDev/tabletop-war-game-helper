import cv2 as cv
import numpy as np


# Returns a list of all yellow circles of the correct radius
# In the format arr[(center, radius)]
def findPieces(img):
   
    
    
    grayFrame = findYellow(img)
    
    blurFrame = cv.GaussianBlur(grayFrame, (17, 17), 0)
    
    # Performing edge detection before Hough Circle Transform reduces computational load
    edges = cv.Canny(blurFrame,100,200)
    
    circles = cv.HoughCircles(edges, cv.HOUGH_GRADIENT,
                              dp = 1.0,
                              minDist=100,
                              minRadius=30, maxRadius=130,
                              param1=100, param2 = 20,)
    
    if circles is None:
        return []
    
    circles = np.uint16(np.around(circles))
    
    
    circleList = []
    for circle in circles[0, :]:
        if circle[2] > 30 and circle[2] < 200:
            circleList.append((circle[0],circle[1],circle[2]))
    return circleList


def findYellow(rgbimage):
    
    blur = cv.GaussianBlur(rgbimage, (5,5), 0)

    hsv_image = cv.cvtColor(blur, cv.COLOR_BGR2HSV)

    # Define the range of yellow color in HSV
    lower_yellow = np.array([24, 76, 128])
    # lower_yellow = np.array([20,50,100])
    upper_yellow = np.array([40, 255, 255])

    # Threshold the HSV image to get only yellow color
    yellow_mask = cv.inRange(hsv_image, lower_yellow, upper_yellow)
    
    
    # cv.imshow("yellow",yellow_mask)
    return yellow_mask

