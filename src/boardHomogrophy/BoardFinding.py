import numpy as np
from numpy import ndarray
import cv2 as cv
# import HomographyUtils

# When we take the original image there are likely to be parts of the image which contain the surroundings of the board.
# When displaying the board we want our 0,0 coordinate to correlate with the top left corner of the board.
# If we take the original image and find the four corners of the board we can then use these to crop the image.
# So when we pass the model positions to the interface we don't have to worry about translating the coordinates (as much).



def getCornerPos(event, x, y, flags, param):    
    # print("I AM AN EVENT")
    # Turns out DBLCKLK is Double Click
    # if event == cv.EVENT_LBUTTONDBLCLK:
    #     print("AAAAAAAAa")
    #     print(x, y)
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
    
    
# 2 Corners
# Take Rectangle
# Use this to crop the image when doing circle detection
# Transform the coordinates of the circles to the size of the display board

# Problems 29/03
# QT is not working
# Tried QT 5 + 6
# Not made for making games like this
# Displaying rectangles and circles causes the program to shift the center in weird ways
# As a result placing things absolute is difficult
# I think everything is relative to eachother

# Explored Pyglet - Somewhat newer type than pygame, documentation isnt quite as good
# Settled on pygame

# Had some time re-doing the colour thresholding only to realise it was fine
# Probably need to re-do the circle detection size checking

# Ideas as is
# Take 4 corners - perspective transform
# AR tags for the corners
# L shaped contrasting corners 
# Detection and game separate - threading, server - will probably cause issues with the display as it is single threaded
# Need to make sure the display is responsive
# Other colours are: Light Blue, Yellow, Pink, Black, White, Same as used in Colour Tags (Find a paper somewhere pls)

# 