import cv2
import numpy as np

def nothing(x):
    pass

# Create a black image, a window
img = cv2.imread("Identification/paperTestPink.jpg")
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('H','image',0,179,nothing)
cv2.createTrackbar('S','image',0,255,nothing)
cv2.createTrackbar('V','image',0,255,nothing)

cv2.createTrackbar('H1','image',0,179,nothing)
cv2.createTrackbar('S1','image',0,255,nothing)
cv2.createTrackbar('V1','image',0,255,nothing)

# initial values
cv2.setTrackbarPos('H', 'image', 27)
cv2.setTrackbarPos('S', 'image', 108)
cv2.setTrackbarPos('V', 'image', 162)

cv2.setTrackbarPos('H1', 'image', 40)
cv2.setTrackbarPos('S1', 'image', 255)
cv2.setTrackbarPos('V1', 'image', 255)

# cv2.createTrackbar('H','yellow',0,179,nothing)
# cv2.createTrackbar('S','yellow',0,255,nothing)
# cv2.createTrackbar('V','yellow',0,255,nothing)

# cv2.createTrackbar('H1','yellow',0,179,nothing)
# cv2.createTrackbar('S1','yellow',0,255,nothing)
# cv2.createTrackbar('V1','yellow',0,255,nothing)

# # initial values
# cv2.setTrackbarPos('H', 'yellow', 27)
# cv2.setTrackbarPos('S', 'yellow', 108)
# cv2.setTrackbarPos('V', 'yellow', 162)

# cv2.setTrackbarPos('H1', 'yellow', 40)
# cv2.setTrackbarPos('S1', 'yellow', 255)
# cv2.setTrackbarPos('V1', 'yellow', 255)

kernal = np.ones((7,7), "uint8")
while(1):
    # Get current positions of the trackbars
    h = cv2.getTrackbarPos('H','image')
    s = cv2.getTrackbarPos('S','image')
    v = cv2.getTrackbarPos('V','image')

    h1 = cv2.getTrackbarPos('H1','image')
    s1 = cv2.getTrackbarPos('S1','image')
    v1 = cv2.getTrackbarPos('V1','image')
    # Convert trackbar positions to HSV
    lower_black = np.array([h, s, v])
    upper_black = np.array([h1, s1, v1])

    lower_yellow = np.array([25, 42, 46])
    upper_yellow = np.array([36, 255, 255])

    blur = cv2.GaussianBlur(img, (7, 7), 0)
    
    # Create a black image with the same size as the original image
    mask = cv2.inRange(cv2.cvtColor(img, cv2.COLOR_BGR2HSV), lower_black, upper_black)
    # maskCopy = cv2.inRange(cv2.cvtColor(img, cv2.COLOR_BGR2HSV), lower_yellow, upper_yellow)
    
    # lower2 = np.array([h1,s1,v1])
    # upper2 = np.array([10,255,255])
    
    # bottomMask = cv2.inRange(cv2.cvtColor(img, cv2.COLOR_BGR2HSV), lower2, upper2)
    
    # mask = mask + bottomMask
    # mask = cv2.bitwise_or(mask, bottomMask)
    
    
    # result = cv2.bitwise_and(img, img, mask=mask)
    # mask = cv2.dilate(mask,kernal )
    
    # mask = cv2.bitwise_not(mask)
    
    # Apply the mask to the original image
    # result = cv2.bitwise_and(img, img, mask=mask)

    # Display the resulting image
    # resized = cv2.resize(mask, (int(mask.shape[1]/2), int(mask.shape[0]/4)))
    cv2.imshow('image', mask)
    # cv2.imshow('yellow', maskCopy)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()

# 155 0 64 for pink