import cv2 as cv 
from cv2 import aruco
import numpy as np
import joblib
import math
import time
from scipy.spatial.transform import Rotation   


# A lot of this is heavy based off of  https://pyimagesearch.com/2020/12/14/generating-aruco-markers-with-opencv-and-python/

# This is mostly a test file 

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
    cv.imshow("ArUCo Tag", image)
    
    image = cv.rotate(image, cv.ROTATE_90_CLOCKWISE)
    arucoDict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_50)
    detectorParams = cv.aruco.DetectorParameters()
    detector = cv.aruco.ArucoDetector(arucoDict, detectorParams)
    imgCopy = image.copy()
    marker_corners, marker_ids = detector.detectMarkers(imgCopy)[:2]
    cv.aruco.drawDetectedMarkers(image = imgCopy, corners= marker_corners, ids= marker_ids)
    print(marker_corners)
    # imgCopy =  cv.resize(imgCopy, (int(imgCopy.shape[1]/2), int(imgCopy.shape[0]/2)))

    camerMatrix = joblib.load("mtx.joblib")
    dist = joblib.load("dist.joblib")

    rvecs,tvecs,trash = my_estimatePoseSingleMarkers(marker_corners, 0.1, camerMatrix, dist)



    cv.drawFrameAxes(imgCopy, camerMatrix, dist, rvecs[0], tvecs[0], 0.1)
    print(rvecs[0][0])

    print(tvecs[0])	


    rMatrix = cv.Rodrigues(rvecs[0][0])

    mtxR, mtxQ, mtxP,qx,qy,qz = cv.RQDecomp3x3(rMatrix[0])
    # coordinate = r.as_euler('xyz', degrees=True)
    
    # might be able to just throw rMatrix into the roation.from_matrix and then take the z value without needing to negate the value or do RQDecomp3x3
    
    r = Rotation.from_matrix(qz)
    coordinate = r.as_euler('xyz', degrees=True)
    # print(r.as_euler('xyz', degrees=True))
    # print(coordinate[2])
    cv.imshow("ArUCo Tag", imgCopy)
    cv.waitKey(0)
    time.sleep(1000)	
  
# https://automaticaddison.com/how-to-convert-a-quaternion-into-euler-angles-in-python/
# Does not work
def uler_from_quaternion(x, y, z, w):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)
     
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)
     
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)
     
        return roll_x, pitch_y, yaw_z # in radians




# https://stackoverflow.com/questions/75750177/solve-pnp-or-estimate-pose-single-markers-which-is-better
def my_estimatePoseSingleMarkers(corners, marker_size, mtx, distortion):
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
    
    for c in corners:
        nada, R, t = cv.solvePnP(marker_points, c, mtx, distortion, False, cv.SOLVEPNP_IPPE_SQUARE)
        rvecs.append(R)
        tvecs.append(t)
        trash.append(nada)
    return np.array([rvecs]), np.array([tvecs]), trash

if __name__ == "__main__":
    detectMarkers(cv.imread("testImages/arucoWithWallAndBorder.jpg"))
    # main()