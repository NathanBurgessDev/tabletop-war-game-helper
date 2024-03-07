import cv2 as cv
import numpy as np


# Returns a list of all yellow circles found within the image, 
# In the format (center, radius)
def findPiece(img):
    
    # Old bad way of doing colour finding - not using HSV space
    # yellowLower = (0, 200, 200)
    # yellowUpper = (100, 255, 255)
    
    # upper = yellowUpper
    # lower = yellowLower
    
    # grayFrame = cv.inRange(img, lower, upper)
    
    grayFrame = findYellow(img)
    
    blurFrame = cv.GaussianBlur(grayFrame, (17, 17), 0)
    
    # Performing edge detection before Hough Circle Transform reduces computational load
    edges = cv.Canny(blurFrame,100,200)
    
    circles = cv.HoughCircles(edges, cv.HOUGH_GRADIENT,
                              dp = 1.0,
                              minDist=100,
                              minRadius=30, maxRadius=400,
                              param1=100, param2=30,)
    
    circles = np.uint16(np.around(circles))
    
    
    circleList = []
    for circle in circles[0, :]:
        circleList.append((circle[0],circle[1],circle[2]))
        
    # print("circle list" + str(circleList))
    
    
    return circleList


def findYellow(rgbimage):
    
    blur = cv.GaussianBlur(rgbimage, (5,5), 0)

    hsv_image = cv.cvtColor(blur, cv.COLOR_BGR2HSV)

    # Define the range of yellow color in HSV
    lower_yellow = np.array([20, 50, 100])
    upper_yellow = np.array([40, 255, 255])

    # Threshold the HSV image to get only yellow color
    yellow_mask = cv.inRange(hsv_image, lower_yellow, upper_yellow)
    
    return yellow_mask


# findPiece("Identification/attempt1.png")
