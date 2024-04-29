import numpy as np
from numpy import ndarray
import cv2 as cv

# When we take the original image there are likely to be parts of the image which contain the surroundings of the board.
# When displaying the board we want our 0,0 coordinate to correlate with the top left corner of the board.
# If we take the original image and find the four corners of the board we can then use these to crop the image.
# So when we pass the model positions to the interface we don't have to worry about translating the coordinates (as much).



def getCornerPos(event, x, y, flags, param):    
    if event == cv.EVENT_LBUTTONDOWN:
        cornerPos.append((x, y))

def getFourCornersCoordinates(image: ndarray):
    global cornerClicks
    global cornerPos
    cornerClicks = 0
    cornerPos = []
   
    cv.namedWindow("Image")
    cv.setMouseCallback("Image", getCornerPos)
    while(1):
        cv.imshow("Image", image)
        k = cv.waitKey(20) & 0xFF
        if len(cornerPos) == 4:
            cv.destroyWindow("Image")
            return cornerPos
        if k ==27:
            break
    # cv.destroyAllWindows()
        



if __name__ == "__main__":
    ()
    # img = cv.imread("testImages/homographyTest.jpg")
    # # resize the image as its 4k
    # img = cv.resize(img, (int(img.shape[1]/2), int(img.shape[0]/2.5)))
    # pts = getFourCornersCoordinates(img)
    # pts = np.array(pts, dtype = "float32")
    # newImg = HomographyUtils.four_point_transform(img, pts)
    # cv.imshow("Image", img)
    # cv.imshow("New Image", newImg)
    # cv.waitKey(0)
    
