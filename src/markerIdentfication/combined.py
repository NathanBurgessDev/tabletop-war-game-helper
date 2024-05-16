import cv2 as cv
from cv2 import aruco
import numpy as np
import math
import path
import sys
import joblib
from scipy.spatial.transform import Rotation  
from math import tan, radians, sqrt

direction = path.Path(__file__).abspath()
sys.path.append(direction.parent.parent)

from markerDetection.findPieces import findPieces
from boardHomogrophy.TopDownView import getTopDownView, calibrateTopDownView


# The board is brown - composite colour - makes it hard to segment from other colours
# As we were originally using red markers this caused issues with segmentation as brown is basically just a dark red

NUM_SEGMENTS = 4
NUM_ENCODING = 5

'''
This file handles both the terrain and model identification
'''


class TerrainTag:
    def __init__(self,id,corners,cameraMatrix, dist):
        self.id = id
        self.cornerPoints = corners
        self.cornerPointsAsTupleList = self.convertToTupleList(corners)
        self.rotation = self.getRotation(cameraMatrix, dist)
    
    def convertToTupleList(self,corners):
        cornerList = []
        for corner in corners[0]:
            cornerList.append((corner[0],corner[1]))
        return cornerList
    
    def getCenterY(self, corners):
        return int((corners[0][1] + corners[2][1]) / 2)
        
    def getCenterX(self, corners):
        return int((corners[0][0] + corners[2][0]) / 2)
        
    def getRotation(self,cameraMatrix, dist):
        rvecs,tvecs,trash = self.my_estimatePoseSingleMarkers(np.array(self.cornerPoints,dtype=np.float32), 0.1, cameraMatrix, dist)
        rMatrix = cv.Rodrigues(rvecs[0][0])
 
        mtxR, mtxQ, mtxP,qx,qy,qz = cv.RQDecomp3x3(rMatrix[0])
    
        r = Rotation.from_matrix(qz)
        return -(r.as_euler('xyz', degrees=True)[2])
    
    def getDistanceBetweenPoints(self, pointOne: tuple[int,int], pointTwo: tuple[int,int]):
        return sqrt((pointOne[0] - pointTwo[0])**2 + (pointOne[1] - pointTwo[1])**2)
    
    
    # https://stackoverflow.com/questions/75750177/solve-pnp-or-estimate-pose-single-markers-which-is-better
    def my_estimatePoseSingleMarkers(self,corners, marker_size, mtx, distortion):        
        '''
        This will estimate the rvec and tvec for each of the marker corners detected by:
            corners, ids, rejectedImgPoints = detector.detectMarkers(image)
        corners - is an array of detected corners for each detected marker in the image
        marker_size - is the size of the detected markers
        mtx - is the camera matrix
        distortion - is the camera distortion matrix
        RETURN list of rvecs, tvecs, and trash (so that it corresponds to the old estimatePoseSingleMarkers())
        '''
        marker_points = np.array([[-marker_size / 2, marker_size / 2, 0],
                                [marker_size / 2, marker_size / 2, 0],
                                [marker_size / 2, -marker_size / 2, 0],
                                [-marker_size / 2, -marker_size / 2, 0]], dtype=np.float32)
        trash = []
        rvecs = []
        tvecs = []
        
        # c needs to be in the format array([[[x.,y.]]])
        for c in corners:
            nada, R, t = cv.solvePnP(marker_points, c, mtx, distortion, False, cv.SOLVEPNP_IPPE_SQUARE)
            rvecs.append(R)
            tvecs.append(t)
            trash.append(nada)
        return np.array([rvecs]), np.array([tvecs]), trash


class ModelEncoding:
    def __init__(self, encoding, circleCenter, circleRadius):
        self.circleCenter = circleCenter
        self.encoding = encoding
        self.circleRadius = circleRadius
        
        
'''
Object to find models and terrain
Contains all the extra information that is needed to do this, such as the camera matrix and distortion coefficients
'''
class ModelFinder:
    def __init__(self, calibrateImage):
        self.cornerPoints = calibrateTopDownView(calibrateImage) # top left, top right, bottom left, bottom right
        self.arucoDict = aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_50)
        self.arucoParams = aruco.DetectorParameters()
        self.arucoDetector = aruco.ArucoDetector(self.arucoDict, self.arucoParams)
        self.cameraMatrix = joblib.load("mtx.joblib")
        self.dist = joblib.load("dist.joblib")
        
    def identifyModels(self,image):
        return identifyAllPieces(image,self.cornerPoints)
    def identifyTerrain(self,image):
        return identifyAllTerrain(image,self.cornerPoints,self.arucoDetector,self.cameraMatrix,self.dist)


'''
Performs the identification of all the terrain
Returns a list of TerrainTag objects

Does our perspective transform to get a top down view
Then uses the aruco detector to find the markers
'''
def identifyAllTerrain(img,pts,detector,cameraMatrix,dist) -> list[TerrainTag] | None:
    image = getTopDownView(img,pts)
    
    marker_corners, marker_ids = detector.detectMarkers(image)[:2]
    if (marker_ids is None):
        return None
    
    terrainList = []
    for i in range (0, len(marker_ids)):
        terrainList.append(TerrainTag(marker_ids[i],marker_corners[i],cameraMatrix,dist))
   
    if (len(terrainList) <= 0):
        return None
   
    return terrainList
    

'''
Performs the locating and identification of all the model markers

Returns a list of ModelEncoding objects

Gets a top downView of the image
Calls the piece finder to get the circle locations and radii
Then finds the pink center points
For each circle it finds the 4 closest pink center points
Then for each pink center point it finds the encodings to the right and left
It then groups the encodings by position and checks for errors
'''
def identifyAllPieces(img, pts) -> tuple[list[ModelEncoding], tuple[int,int] | None, tuple[int,int]]:
    
    
    image = getTopDownView(img,pts)
    
    imageSize = image.shape
    
    circles = findPieces(image)
    
    if (len(circles) <= 0):
        return (None, imageSize)
 
    
    
    pinkFrame = findPink(image)

    kernal = np.ones((3,3), "uint8")
  
    dilatedRedFrame = cv.dilate(pinkFrame,kernal)
    try:
        redCenterPoints = findRedContourCentroids(dilatedRedFrame)
    except:
        print("No pink center points found")
        return (None, imageSize)
    
  
    
    
    blur = cv.GaussianBlur(image, (7, 7), 0)
    hsvImage = cv.cvtColor(blur, cv.COLOR_BGR2HSV)
    
    encodingList = []
    for circle in circles:
        try:
            contourCentersAsQuarters = getCentersOfCircleBitContours((circle[0],circle[1]), circle[2],redCenterPoints, image)
        except:
            print("Problem getting contourCenters - Probably no pink centroids near enough")
            continue
        
        right = contourCentersAsQuarters[0]
        left = contourCentersAsQuarters[1]
        
       
        quarterEncodingListRight = []
        for quarter in right:
            encodingsInQuarter = getFullEncoding(hsvImage, quarter)
            quarterEncodingListRight.append(encodingsInQuarter)
    
       
        quarterEncodingListLeft = []
        for quarter in left:
           
            encodingsInQuarter = getFullEncoding(hsvImage, quarter)
            quarterEncodingListLeft.append(encodingsInQuarter)
        
        correlatedQuarters = zip(quarterEncodingListRight,quarterEncodingListLeft)
        quartersTuple = tuple(correlatedQuarters)
        
        # Perform some error checking
        # We have read to the left and right of each red center point
        # To make sure we have the correct encoding we will need to check each quarter for any missing encodings
        # print(quartersTuple)
        
        if (len(quartersTuple) <= 0):
            print("Encoding Is empty")
            continue
        
        encoding = checkForErrorsForBit(groupEncodingBits(quartersTuple))
        
        finalEncoding = ModelEncoding(encoding, (circle[0],circle[1]), circle[2])
       
    
        encodingList.append(finalEncoding)
    
    
    return (encodingList, imageSize)
    

# We need to group the bits together by their positions on the encoding
# I.e all the first positions bits together from the left and right read
# for example 1 2 3 4 , 1 2 3 4, 1 2 2 3, 1 2 3 4
# would become: 1,1,1,1, 2,2,2,2, 3,3,2,3 ,4,4,3,4
# For some reason this took a long time to write
# I wasted a lot of time on the checkForErrorsInQuarter function which was a bad way of doing this
# Then ended up with the 2 for loops the wrong way round
def groupEncodingBits(quartersTuple):
    groupedBits = []
    for i in range (0, len(quartersTuple[0][0])):
        bitArray = []
        for quarter in quartersTuple:
            bitArray.append(quarter[0][i])
            bitArray.append(list(reversed(quarter[1]))[i])
        groupedBits.append(bitArray)
    return groupedBits
            
        
# Takes in our grouped bits by position
# Returns the most common encoding for each position to be used as a final encoding
def checkForErrorsForBit(groupedBits):
    finalEncoding = []
    for group in groupedBits:
        ones = group.count(1)
        twos = group.count(2)
        if ones >= twos:
            finalEncoding.append(1)
        else:
            finalEncoding.append(2)
    return finalEncoding


''' DEPRECATED FUNCTION
was originally at a sort of homebrew attempt at hamming distance without really knowing what that was
'''

# @DeprecationWarning("This methodology was not a good approach, although it is left here for reference")
def checkForErrorsInQuarter(quarter):
    right = quarter[0]
    left = quarter[1]
    bothFailed = False
    
    # Check if there is a missing encoding in both
    # Need to see if we can combine encodings to get a full encoding
    # If both contain 0 we can not bother checking the rest
    rebuiltEncodingList = [[]]
    if (0 in left and 0 in right):
        rebuiltEncodingList.append([])
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
# For each pink center point check the colours to the right
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


# Before:
# real    0m2.290s
# user    0m3.089s
# sys     0m1.195s

# After:
# real    0m0.678s
# user    0m1.374s
# sys     0m1.293s

def getEncodingAtPoint(hsvImage, point):

    # If a part of the identifcation ring is outside of the image - when calculating the position of the non pink points
    # This will cause an error as its trying to look outside of the image
    # Bounds checking is needed
    
    if (point[1] >= hsvImage.shape[0] or point[0] >= hsvImage.shape[1]):
        return 0
        
    hsvPoint = hsvImage[point[1], point[0]]

    # Encoding 1 boundaries - currently Black
    # Made a slider program to test values
    lower1 = np.array([0, 0, 80])
    upper1 = np.array([179, 255, 255])
 
    # 81 works well
    # 90 is too high
    
    # Encoding 2 Upper boundaries - currently White
    
    lower2 = np.array([0,46,0])
    upper2 = np.array([179, 255, 255])
    
    
    if (not hsvPointInRange(hsvPoint, lower1, upper1)):
        return 1
    if (not hsvPointInRange(hsvPoint, lower2, upper2)):
        return 2    
    # 0 is for something not correctly identified
    else:
        return 0
    

'''
Returns the pink mask of the image
'''
def findPink(rgbImage):
    blur = cv.GaussianBlur(rgbImage, (7, 7), 0)
    hsvImage = cv.cvtColor(blur, cv.COLOR_BGR2HSV)
    
    lower1 = np.array([83, 68, 63])
    upper1 = np.array([179,255,255])
    
    pinkMask = cv.inRange(hsvImage,lower1, upper1)
    return pinkMask

# An improvement would be to check the rough shape of the contours as to not get the wrong ones
'''
Finds the centroids of the provided contours
Used for finding the pink encoding bits
'''
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
            redCenterPoints.append((cx, cy))
            cv.drawContours(img, [c], -1, (255, 255, 255), 5)
    except:
        print(":3")
        pass
    
    


    
    return redCenterPoints


# For each pink center point check the colour of the contours to the right
# Returns the positions of these new contours
def getRightContoursPositions(redCenterPoints, center, radius, image):
    data = []
    for x, y in redCenterPoints:
        quarter = []
      
        x = x - center[0]
        y = y - center[1]
        for i in range(0, int(360 / NUM_SEGMENTS), int(int(360 / NUM_SEGMENTS) / NUM_ENCODING)):
            newPosX =x * math.cos(math.radians(i)) - y * math.sin(math.radians(i))
            newPosY =x * math.sin(math.radians(i)) + y * math.cos(math.radians(i))
           
            quarter.append((int(newPosX) + center[0], int(newPosY)+center[1]))
        data.append(quarter)
    return data

def getLeftContoursPositions(redCenterPoints, center):
    data = []
    for x, y in redCenterPoints:
        quarter = []
        x = x - center[0]
        y = y - center[1]
        for i in range(0,-int(360 / NUM_SEGMENTS), -int(int(360 / NUM_SEGMENTS) / NUM_ENCODING)):
      
            newPosX =x * math.cos(math.radians(i)) - y * math.sin(math.radians(i))
            newPosY =x * math.sin(math.radians(i)) + y * math.cos(math.radians(i))

            quarter.append((int(newPosX) + center[0], int(newPosY)+center[1]))
        data.append(quarter)
    return data

if __name__ == "__main__":
    identifyAllPieces()