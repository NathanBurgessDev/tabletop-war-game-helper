import cv2 as cv 
from cv2 import aruco
import numpy as np

# A lot of this is heavy based off of  https://pyimagesearch.com/2020/12/14/generating-aruco-markers-with-opencv-and-python/


# This lists all the ArUco dictionaries that can be used
# NXN - 2D bit size -> basically the grid size of the marker
#  Following int -> total number of unique ID's

# Smaller dictionary sizes with larger NxN marker sizes increase the inter-marker distance, thereby making them less prone to false readings.
# Basically, the larger the NxN marker size the more bits there are to read. If we use a small dictionary size with a large NxN marker size, we have a lot of bits to read but not many unique markers
# i.e. if we have 36 bits , and a dictijnary of 250, you only need 8 bits to represent each marker
# This leaves us with 28 bits which aren ot used which can be utilised for error correction
# Even if some of the bits are wrong we can find a pattern in our dictionary that is closest to the pattern we have
ARUCO_DICT = {
	"DICT_4X4_50": cv.aruco.DICT_4X4_50,
	"DICT_4X4_100": cv.aruco.DICT_4X4_100,
	"DICT_4X4_250": cv.aruco.DICT_4X4_250,
	"DICT_4X4_1000": cv.aruco.DICT_4X4_1000,
	"DICT_5X5_50": cv.aruco.DICT_5X5_50,
	"DICT_5X5_100": cv.aruco.DICT_5X5_100,
	"DICT_5X5_250": cv.aruco.DICT_5X5_250,
	"DICT_5X5_1000": cv.aruco.DICT_5X5_1000,
	"DICT_6X6_50": cv.aruco.DICT_6X6_50,
	"DICT_6X6_100": cv.aruco.DICT_6X6_100,
	"DICT_6X6_250": cv.aruco.DICT_6X6_250,
	"DICT_6X6_1000": cv.aruco.DICT_6X6_1000,
	"DICT_7X7_50": cv.aruco.DICT_7X7_50,
	"DICT_7X7_100": cv.aruco.DICT_7X7_100,
	"DICT_7X7_250": cv.aruco.DICT_7X7_250,
	"DICT_7X7_1000": cv.aruco.DICT_7X7_1000,
	"DICT_ARUCO_ORIGINAL": cv.aruco.DICT_ARUCO_ORIGINAL,
	"DICT_APRILTAG_16h5": cv.aruco.DICT_APRILTAG_16h5,
	"DICT_APRILTAG_25h9": cv.aruco.DICT_APRILTAG_25h9,
	"DICT_APRILTAG_36h10": cv.aruco.DICT_APRILTAG_36h10,
	"DICT_APRILTAG_36h11": cv.aruco.DICT_APRILTAG_36h11
}

def main():
    # arucoDict = cv.aruco.Dictionary(cv.aruco.DICT_4X4_50)
    arucoDict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_50)
    tag = np.zeros((200, 200, 3), dtype="uint8")
    # tag[:, :] = [255, 255, 255]
    
    marker = cv.aruco.generateImageMarker(arucoDict, 1, 200, tag, 1)
    # cv.imwrite("marker23.png", tag)
    # cv.imshow("ArUCo Tag", marker)
    
    
    detectorParams = cv.aruco.DetectorParameters()
    detector = cv.aruco.ArucoDetector(arucoDict, detectorParams)
    imgCopy = marker.copy()
    marker_corners, marker_ids = detector.detectMarkers(imgCopy)[:2]
    
    print(marker_ids)
    
    cv.aruco.drawDetectedMarkers(image = imgCopy, corners= marker_corners, ids= marker_ids)
    
    cv.imshow("ArUCo Tag", marker)
    cv.imwrite("marker1.png", marker)
    cv.waitKey(0)
    
def detectMarkers(image):
	image = cv.rotate(image, cv.ROTATE_90_CLOCKWISE)
	arucoDict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_50)
	detectorParams = cv.aruco.DetectorParameters()
	detector = cv.aruco.ArucoDetector(arucoDict, detectorParams)
	imgCopy = image.copy()
	marker_corners, marker_ids = detector.detectMarkers(imgCopy)[:2]
	cv.aruco.drawDetectedMarkers(image = imgCopy, corners= marker_corners, ids= marker_ids)
	imgCopy =  cv.resize(imgCopy, (int(imgCopy.shape[1]/2), int(imgCopy.shape[0]/2)))
	cv.imshow("ArUCo Tag", imgCopy)
	cv.waitKey(0)	
  



if __name__ == "__main__":
    detectMarkers(cv.imread("testImages/oneCoverWall.jpg"))
    # main()