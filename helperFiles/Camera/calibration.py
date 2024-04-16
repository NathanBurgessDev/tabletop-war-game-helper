import numpy as np
import cv2 as cv
import glob
import joblib


# https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html
def calibrate():
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    CHECKERBOARD = (6,9)

    objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
    objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    images = glob.glob('helperFiles/Camera/calibrationImages/*.jpg')
    print(images)

    for fname in images:
        # print(fname)
        img = cv.imread(fname)
        # cv.imshow('img', img)
        # cv.waitKey(0)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # print(fname)
        
        # Find the chess board 
        ret, corners = cv.findChessboardCorners(gray, CHECKERBOARD, None)
        # print(fname)
        
        # If found, add object points, image points (after refining them)
        if ret == True:
            print(fname)
            objpoints.append(objp)
        
            corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners2)
            
            # Draw and display the corners
            cv.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
            cv.imshow('img', img)
            cv.waitKey(500)
        
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    # joblib.dump(ret, "ret.joblib")

    joblib.dump(mtx, "mtx.joblib")
    print(mtx)

    joblib.dump(dist, "dist.joblib")
    print(dist)


    joblib.dump(rvecs, "rvecs.joblib")
    print(rvecs)

    joblib.dump(tvecs, "tvecs.joblib")
    print(tvecs)


    cv.destroyAllWindows()

def getCameraMatrix():
    mtx = joblib.load("mtx.joblib")
    print(mtx)
    dist = joblib.load("dist.joblib")
    print(dist)
    
    img = cv.imread("helperFiles/Camera/calibrationImages/IMG_3628.jpg")
    h,w = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    
    joblib.dump(newcameramtx, "newcameramtx.joblib")
    
    dst = cv.undistort(img,mtx,dist,newcameramtx)
    # x, y, w, h = roi
    # dst = dst[y:y+h, x:x+w]
    
    cv.imshow("undistorted", dst)
    cv.imshow("original", img)
    cv.waitKey(0)
    

if __name__ == "__main__":
    getCameraMatrix()