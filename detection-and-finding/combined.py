import cv2 as cv
import numpy as np
import findPieces
import math

def identifyAllPieces():
    
    filePath = "Identification/paperTest.jpg"
    
    image = cv.imread(filePath)
    
    circles = findPieces.findPieces(image)
    print(circles)
    
    # For testing please change this later ty ty
    # center = (circles[0][0], circles[0][1])
    
    # radius = circles[0][2] * 2
    
    # cropped = image[center[1]-radius:center[1]+radius, center[0]-radius:center[0]+radius]
    
    
    redFrame = findRed(image)

    redCenterPoints = findRedContourCentroids(redFrame)
    
    
    modelIdData = []
    
    for circle in circles:
        modelIdData.append(identifyPiece((circle[0],circle[1]), circle[2],redCenterPoints, image))
        
    for dataPoints in modelIdData:
        # cv.circle(image, (point[0], point[1]), 1, (0, 255, 0), 3)
        for point in dataPoints:
            cv.circle(image, (point[0], point[1]), 1, (0, 255, 0), 3)
            
    # print(modelIdData)
        
    
    
    # Find the red Center point closest to the center of the circle
    # redCenterPoints.sort(key=lambda x: math.sqrt((x[0] - center[0])**2 + (x[1] - center[1])**2))
    # print(redCenterPoints)
    # print(center)
    
 
    
    
    
    # cv.imshow("red",redFrame)
    resized = cv.resize(image, (int(image.shape[1]/2), int(image.shape[0]/2)))
    cv.imshow("img",resized)
    # cv.imshow("cropped",cropped)
    
    
    
    # cv.imshow("rotate",rotate)


    k = cv.waitKey(0)
    
    
def identifyPiece(center, radius, centroids, image):
    
    centroids.sort(key=lambda x: math.sqrt((x[0] - center[0])**2 + (x[1] - center[1])**2))
    
    identifiedCircleData = identifyCircle(centroids, center, radius, image)
    

    
    return identifiedCircleData
    pass
    


# Ty Adrian for the code - I stole it from your semaphore flags
def findRed(rgbImage):
    blur = cv.GaussianBlur(rgbImage, (7, 7), 0)
    hsvImage = cv.cvtColor(blur, cv.COLOR_BGR2HSV)
    
    # lower boundary RED color range values; Hue (0 - 10)
    lower1 = np.array([0, 70, 70])
    upper1 = np.array([15, 255, 255])
 
    # upper boundary RED color range values; Hue (160 - 180)
    lower2 = np.array([160,70,70])
    upper2 = np.array([179,255,255])
    
    # Threshold the HSV image to get only red color
    top_mask = cv.inRange(hsvImage, lower1, upper1)
    bot_mask = cv.inRange(hsvImage, lower2, upper2)

    red_mask = top_mask + bot_mask
    
    # cv.imshow("red",red_mask)
    
    return red_mask


def findRedContourCentroids(img):
    
    cnts = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
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
            # cv.drawContours(img, [c], -1, (255, 255, 255), 5)
    except:
        print(":3")
        pass
    
    return redCenterPoints
        
def identifyCircle(redCenterPoints, center, radius, image):
    data = []
    for x, y in redCenterPoints[0:4]:
        print(f"Red Box : x={x}, y={y}")
        x = x - center[0]
        y = y - center[1]
        for i in range(0, 90, 18):
            newPosX =x * math.cos(math.radians(i)) - y * math.sin(math.radians(i))
            newPosY =x * math.sin(math.radians(i)) + y * math.cos(math.radians(i))
            # cv.circle(image, (int(newPosX) + center[0], int(newPosY)+center[1]), 1, (0, 255, 0), 3)
            data.append((int(newPosX) + center[0], int(newPosY)+center[1]))
    return data

identifyAllPieces()