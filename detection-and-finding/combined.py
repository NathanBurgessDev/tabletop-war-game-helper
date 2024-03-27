import cv2 as cv
import numpy as np
import findPieces
import math

# The board is brown - composite colour - very annoying

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
    kernal = np.ones((3,3), "uint8")
    
    #I have no Idea why dilating makes this work but it does
    dilatedRedFrame = cv.dilate(redFrame,kernal )
    redCenterPoints = findRedContourCentroids(dilatedRedFrame)
    
    decodedCircles = []
    
    
    blur = cv.GaussianBlur(image, (7, 7), 0)
    hsvImage = cv.cvtColor(blur, cv.COLOR_BGR2HSV)
    
    # For each circle take the 4 closest red center points within a certain radius
    # For each red center point check the colour of the contours to the right
    # For each red center point check the colour of the contours to the left
    # Perform some error checking
    
    # We need some kind of error checking to make sure our encodings are correct
    # We will read to the right of a centroid
    # If there is a 0 returned in this we will compare the left read and the right read
    # If we can find a complete encoding by combining the two we will do so
    for circle in circles:
        contourCentersAsQuarters = getCentersOfCircleBitContours((circle[0],circle[1]), circle[2],redCenterPoints, image)
        
        right = contourCentersAsQuarters[0]
        left = contourCentersAsQuarters[1]
        
       
        quarterEncodingListRight = []
        for quarter in right:
            # for point in quarter:
                # cv.circle(image, (point[0], point[1]), 1, (0, 0, 255), 3)
            encodingsInQuarter = getFullEncoding(hsvImage, quarter)
            quarterEncodingListRight.append(encodingsInQuarter)
        # print(quarterEncodingListRight)
        
       
        quarterEncodingListLeft = []
        for quarter in left:
           
            encodingsInQuarter = getFullEncoding(hsvImage, quarter)
            quarterEncodingListLeft.append(encodingsInQuarter)
        # print(quarterEncodingListLeft)
        
        # for quarter in left:
        #     for point in quarter:
        #         cv.circle(image, (point[0], point[1]), 1, (0, 255, 0), 3)
        
        correlatedQuarters = zip(quarterEncodingListRight,quarterEncodingListLeft)
        quartersTuple = tuple(correlatedQuarters)
        
        # Perform some error checking
        # We have read to the left and right of each red center point
        # To make sure we have the correct encoding we will need to check each quarter for any missing encodings
        quarterConcensus = []
        for quarter in quartersTuple:
            checkForErrorsInQuarter(quarter)
                

        print("NEXT CIRCLE")
        
        
        
            
        

        
    
    
    imageDisplay = image.copy()    
    

    
    # for dataPoints in decodedCircles:
    #     # cv.circle(image, (point[0], point[1]), 1, (0, 255, 0), 3)
    #     print("NEXT ENCODING")
    #     finalEncodingList= []
    #     finalEncodingList = getFullEncoding(hsvImage, dataPoints)
    #     # cv.circle(imageDisplay, (point[0], point[1]), 1, (0, 255, 0), 3)
    #     print(finalEncodingList)
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
    

# The first bit of error checking we need to do is to see if any of the encoding bits are missing

# Will return a list of potential encodings for the provided quarter
# more "robust" encodings will be returned twice, as to influence the voting
def checkForErrorsInQuarter(quarter):
    right = quarter[0]
    left = quarter[1]
    bothFailed = False
    # I have no idea why .reverse() does not work here
    
    # Check if there is a missing encoding in both
    # Need to see if we can combine encodings to get a full encoding
    # If both contain 0 we can not bother checking the rest
    rebuiltEncodingList = [[]]
    if (0 in left and 0 in right):
        bothFailed = True
        print("both contain 0")
        
        # See if we can combine the two
        # To do this we need to check which bits are missing on which encoding
        for i in range(0, len(left)):
            if (list(reversed(left))[i] == 0 and right[i] != 0):
                print("left missing encoding")
                for encoding in rebuiltEncodingList:
                    encoding.append(right[i])
                
            elif (list(reversed(left))[i] != 0 and right[i] == 0):
                print("right missing encoding")
                for encoding in rebuiltEncodingList:
                    encoding.append(list(reversed(left))[i])
                    
            elif (list(reversed(left))[i] == 0 and right[i] == 0):
                print("both missing encoding")
                for encoding in rebuiltEncodingList:
                    encoding.append(0)
                    
            # We now need to check if the two encodings are the same
            else:
                # If this is the case then this bit has been misread somehow
                # We will need to check the other quarters to see which one they match
                # We will now need to return the potential encodings with both possible
                # interpretations of that decoded bit
                if (list(reversed(left))[i] != right[i]):
                    print("left and right do not match")
                    copyOfRebuiltEncodingList = rebuiltEncodingList.copy()
                    
                    for encoding in rebuiltEncodingList:
                        encoding.append(right[i])
                        
                    for encoding in copyOfRebuiltEncodingList:
                        encoding.append(list(reversed(left))[i])
                    
                    rebuiltEncodingList = rebuiltEncodingList + copyOfRebuiltEncodingList
                    
                    
                # If they are the same we can just add one to the list
                else:
                    for encoding in rebuiltEncodingList:
                        encoding.append(right[i])
                        
            return rebuiltEncodingList


    
    # In this case one of the encodings is complete
    if (not bothFailed):
        
        # If there is a missing encoding in the left
        # See if the right is fine
        
        # If the left has the 0 then the right must have a full encoding
        if 0 in left:
            rebuiltEncodingList.append(right)
            return rebuiltEncodingList
        
        # If the right has the 0 then the left must have a full necoding
        elif 0 in right:
            rebuiltEncodingList.append(list(reversed(left)))

            return rebuiltEncodingList

        # If left and right do not match and there is no 0 in either
        # They have been read "correctly" but something has been misread
        
        # An alternaative approach could be to treat bits that are different as 0
        # and then return all the possible encodings
        
        # We will insert both into the concensus list
        # So the final choice can be voted on by the most common decoding   
        elif (list(reversed(left)) != right):
            print("left and right do not match")
            
        # In this case both encodings match with no errors
        else:
            rebuiltEncodingList.append(right)
            rebuiltEncodingList.append(list(reversed(left)))
            
    return rebuiltEncodingList
    


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
        
    circleBitCoordinatesRight = getRightContoursPositions(correctCentroids, center, radius, image)
    
    circleBitCoordinatesLeft = getLeftContoursPositions(correctCentroids, center)
    
    return (circleBitCoordinatesRight, circleBitCoordinatesLeft)


# Removed converting to hsv from this loop
# Saved a significant amount of time
# After
# real    0m0.671s
# user    0m1.390s
# sys     0m1.306s

# Before:
# real    0m1.191s
# user    0m2.973s
# sys     0m2.844s

def getFullEncoding(hsvImage, data):
    encoding = []
    # Remove the first point used to find where to start reading
    data.pop(0)
    for point in data:
        encoding.append(getEncodingAtPoint(hsvImage, point))
    
    return encoding
    
    


def hsvPointInRange(hsvPoint, lower, upper):
    return (hsvPoint[0] >= lower[0] and hsvPoint[0] <= upper[0] and hsvPoint[1] >= lower[1] and hsvPoint[1] <= upper[1] and hsvPoint[2] >= lower[2] and hsvPoint[2] <= upper[2])

# Doing this constant in range check is very very slow
# This needs to be re-written

# With print statements

# Before:
# real    0m2.290s
# user    0m3.089s
# sys     0m1.195s

# After:
# real    0m0.678s
# user    0m1.374s
# sys     0m1.293s
def getEncodingAtPoint(hsvImage, point):
    
    
    hsvPoint = hsvImage[point[1], point[0]]
    
    
    
    # Encoding 1 boundaries - currently Black
    # Made a slider program to test values
    lower1 = np.array([0, 0, 80])
    upper1 = np.array([179, 255, 255])
    
    
    # blackMask = hsvPointInRange(hsvPoint, lower1, upper1)
    
    # 81 works well
    # 90 is too high
    
    # Encoding 2 Upper boundaries - currently White
    
    lower2 = np.array([0,46,0])
    upper2 = np.array([179, 255, 255])
    
    # blackMask = cv.inRange(hsvImage, lower1, upper1)

    # blackMask = cv.bitwise_not(blackMask)
    
    # whiteMask = cv.inRange(hsvImage, lower2, upper2)
    
    # whiteMask = cv.bitwise_not(whiteMask)
    
    # lowBit = (blackMask[point[1], point[0]])
    # highBit = (whiteMask[point[1], point[0]])
    
    # whiteMask = cv.resize(whiteMask, (int(whiteMask.shape[1]/2), int(whiteMask.shape[0]/4)))
    # cv.imshow("black",whiteMask)
    
    
    # if (lowBit == 255):
    #     return 1
    # if (highBit == 255):
    #     return 2
    
    if (not hsvPointInRange(hsvPoint, lower1, upper1)):
        return 1
    if (not hsvPointInRange(hsvPoint, lower2, upper2)):
        return 2    
    # 0 is for something not correctly identified
    else:
        return 0
    
    # cv.imshow("black",blackMask)
    # return (blackMask[point[1], point[0]])
    


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

# An improvement would be to check the rough shape of the contours as to not get the wrong ones
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
            # print(f"Red Box {i} : cx={cx}, cy={cy}") 
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

def getLeftContoursPositions(redCenterPoints, center):
    data = []
    for x, y in redCenterPoints:
        quarter = []
        # print(f"Red Box : x={x}, y={y}")
        x = x - center[0]
        y = y - center[1]
        for i in range(0,-int(360 / NUM_SEGMENTS), -int(int(360 / NUM_SEGMENTS) / NUM_ENCODING)):
      
            newPosX =x * math.cos(math.radians(i)) - y * math.sin(math.radians(i))
            newPosY =x * math.sin(math.radians(i)) + y * math.cos(math.radians(i))
            # cv.circle(image, (int(newPosX) + center[0], int(newPosY)+center[1]), 1, (0, 255, 0), 3)
            quarter.append((int(newPosX) + center[0], int(newPosY)+center[1]))
        data.append(quarter)
    return data


identifyAllPieces()