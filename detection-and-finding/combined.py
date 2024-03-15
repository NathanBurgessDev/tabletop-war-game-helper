import cv2 as cv
import numpy as np
import findPieces
import math

# The board is brown - composite colour

NUM_SEGMENTS = 4
NUM_ENCODING = 5

# First bit - Team (1 or 2)
class ModelEncoding:
    def __init__(self, encoding, circleCenter, circleRadius):
        self.circleCenter = circleCenter
        self.encoding = encoding
        self.circleRadius = circleRadius


def identifyAllPieces():
    
    filePath = "Identification/paperTestPinkCover.jpg"
    
    image = cv.imread(filePath)
    
    circles = findPieces.findPieces(image)
    print(circles)
    
    # For testing please change this later ty ty
    # center = (circles[0][0], circles[0][1])
    
    # radius = circles[0][2] * 2
    
    # cropped = image[center[1]-radius:center[1]+radius, center[0]-radius:center[0]+radius]
    
    
    redFrame = findPink(image)

#   
    kernal = np.ones((7,7), "uint8")
    
    #I have no Idea why dilating makes this work but it does
    dilatedRedFrame = cv.dilate(redFrame,kernal )
    redCenterPoints = findRedContourCentroids(dilatedRedFrame)
    
    decodedCircles = []
    
    
    # For each circle take the 4 closest red center points within a certain radius
    # For each red center point check the colour of the contours to the right
    # For each red center point check the colour of the contours to the left
    # Perform some error checking
    for circle in circles:
        contourCentersAsQuarters = getCentersOfCircleBitContours((circle[0],circle[1]), circle[2],redCenterPoints, image)

        
        quarterEncodingList = []
        for quarter in contourCentersAsQuarters:
            # for point in quarter:
            #     cv.circle(image, (point[0], point[1]), 1, (0, 255, 0), 3)
            encodingsInQuarter = getFullEncoding(image, quarter)
            quarterEncodingList.append(encodingsInQuarter)
        print(quarterEncodingList)
        
            
        

        
    
    
    imageDisplay = image.copy()    
    
    for dataPoints in decodedCircles:
        # cv.circle(image, (point[0], point[1]), 1, (0, 255, 0), 3)
        print("NEXT ENCODING")
        finalEncodingList= []
        finalEncodingList = getFullEncoding(image, dataPoints)
        # cv.circle(imageDisplay, (point[0], point[1]), 1, (0, 255, 0), 3)
        print(finalEncodingList)
    # print(modelIdData)
        
    for dataPoints in decodedCircles:
        for point in dataPoints:
            cv.circle(image, (point[0], point[1]), 1, (0, 255, 0), 3)
    
    
    # Find the red Center point closest to the center of the circle
    # redCenterPoints.sort(key=lambda x: math.sqrt((x[0] - center[0])**2 + (x[1] - center[1])**2))
    # print(redCenterPoints)
    # print(center)
    
 
    
    
    
    # cv.imshow("red",redFrame)
    resized = cv.resize(image, (int(image.shape[1]/2), int(image.shape[0]/2)))
    # cv.imshow("img",resized)
    # cv.imshow("cropped",cropped)
    
    
    
    # cv.imshow("rotate",rotate)


    k = cv.waitKey(0)
    




# Takes a center and a radius and a list of red center points
# Takes the 4 closest red center points 
# // TODO (make this work for a certain radius as a limit)
# For each red center point check the colours to the right
def getCentersOfCircleBitContours(center, radius, centroids, image):
    
    centroids.sort(key=lambda x: math.sqrt((x[0] - center[0])**2 + (x[1] - center[1])**2))
    correctCentroids = []
    for centroid in centroids[0:NUM_SEGMENTS]:
        distance = math.sqrt((centroid[0] - center[0])**2 + (centroid[1] - center[1])**2)
        if (distance < radius + 50):
            correctCentroids.append(centroid)
        
    circleBitCoordinates = getRightContoursPositions(correctCentroids, center, radius, image)
    
    return circleBitCoordinates


def getFullEncoding(rgbImage, data):
    blur = cv.GaussianBlur(rgbImage, (7, 7), 0)
    hsvImage = cv.cvtColor(blur, cv.COLOR_BGR2HSV)
    
    encoding = []
    # data.pop(0)
    for point in data:
        encoding.append(getEncodingAtPoint(hsvImage, point))
        
    return encoding
    
    


def getEncodingAtPoint(hsvImage, point):
    
    
    # Encoding 1 boundaries - currently Black
    # Made a slider program to test values
    lower1 = np.array([0, 0, 80])
    upper1 = np.array([179, 255, 255])
    
    # 81 works well
    # 90 is too high
    
    # Encoding 2 Upper boundaries - currently White
    
    lower2 = np.array([0,46,0])
    upper2 = np.array([179, 255, 255])
    
    blackMask = cv.inRange(hsvImage, lower1, upper1)

    blackMask = cv.bitwise_not(blackMask)
    
    whiteMask = cv.inRange(hsvImage, lower2, upper2)
    
    whiteMask = cv.bitwise_not(whiteMask)
    
    lowBit = (blackMask[point[1], point[0]])
    highBit = (whiteMask[point[1], point[0]])
    
    whiteMask = cv.resize(whiteMask, (int(whiteMask.shape[1]/2), int(whiteMask.shape[0]/4)))
    # cv.imshow("black",whiteMask)
    if (lowBit == 255):
        return 1
    if (highBit == 255):
        return 2
    
    # 0 is for something not correctly identified
    else:
        return 0
    
    # cv.imshow("black",blackMask)
    return (blackMask[point[1], point[0]])
    


# Ty Adrian for the code - I stole it from your semaphore flags
# def findRed(rgbImage):
#     blur = cv.GaussianBlur(rgbImage, (7, 7), 0)
#     hsvImage = cv.cvtColor(blur, cv.COLOR_BGR2HSV)
    
#     # lower boundary RED color range values; Hue (0 - 10)
#     lower1 = np.array([0, 70, 70])
#     upper1 = np.array([15, 255, 255])
 
#     # upper boundary RED color range values; Hue (160 - 180)
#     lower2 = np.array([160,70,70])
#     upper2 = np.array([179,255,255])
    
#     # Threshold the HSV image to get only red color
#     top_mask = cv.inRange(hsvImage, lower1, upper1)
#     bot_mask = cv.inRange(hsvImage, lower2, upper2)

#     red_mask = top_mask + bot_mask
    
#     # cv.imshow("red",red_mask)
    
#     return red_mask


def findPink(rgbImage):
    blur = cv.GaussianBlur(rgbImage, (7, 7), 0)
    hsvImage = cv.cvtColor(blur, cv.COLOR_BGR2HSV)
    
    lower1 = np.array([83, 68, 63])
    upper1 = np.array([179,255,255])
    
    pinkMask = cv.inRange(hsvImage,lower1, upper1)
    # resized = cv.resize(pinkMask, (int(pinkMask.shape[1]/2), int(pinkMask.shape[0]/4)))
    # cv.imshow('image', resized)
    # cv.waitKey(0)
    return pinkMask

def findRedContourCentroids(img):
    
    cnts = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    for i,c in enumerate(cnts[0]):
        cv.drawContours(img, [c], -1, (255, 255, 255), 5)
    
    redCenterPoints = []
    
    try:
        for i, c in enumerate(cnts[0]):
            # compute the center of the contour
            M = cv.moments(c)
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            print(f"Red Box {i} : cx={cx}, cy={cy}") 
            # cv.circle(img, (cx, cy), 1, (0, 255, 0), 3)
            redCenterPoints.append((cx, cy))
            cv.drawContours(img, [c], -1, (255, 255, 255), 5)
    except:
        print(":3")
        pass
    
    


    
    return redCenterPoints


# For each red center point check the colour of the contours to the right
# Returns the positions of these new contours
def getRightContoursPositions(redCenterPoints, center, radius, image):
    data = []
    for x, y in redCenterPoints:
        quarter = []
        # print(f"Red Box : x={x}, y={y}")
        x = x - center[0]
        y = y - center[1]
        for i in range(0, int(360 / NUM_SEGMENTS), int(int(360 / NUM_SEGMENTS) / NUM_ENCODING)):
            newPosX =x * math.cos(math.radians(i)) - y * math.sin(math.radians(i))
            newPosY =x * math.sin(math.radians(i)) + y * math.cos(math.radians(i))
            # cv.circle(image, (int(newPosX) + center[0], int(newPosY)+center[1]), 1, (0, 255, 0), 3)
            quarter.append((int(newPosX) + center[0], int(newPosY)+center[1]))
        data.append(quarter)
    return data

identifyAllPieces()