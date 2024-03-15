import cv2
import numpy as np

def nothing(x):
    pass

# Create a black image, a window
img = cv2.imread("Identification/paperTestPinkCover.jpg")
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('H','image',0,179,nothing)
cv2.createTrackbar('S','image',0,255,nothing)
cv2.createTrackbar('V','image',0,255,nothing)

# initial values
cv2.setTrackbarPos('H', 'image', 0)
cv2.setTrackbarPos('S', 'image', 0)
cv2.setTrackbarPos('V', 'image', 0)

while(1):
    # Get current positions of the trackbars
    h = cv2.getTrackbarPos('H','image')
    s = cv2.getTrackbarPos('S','image')
    v = cv2.getTrackbarPos('V','image')

    # Convert trackbar positions to HSV
    lower_black = np.array([h, s, v])
    upper_black = np.array([179, 255, 255])

    # Create a black image with the same size as the original image
    mask = cv2.inRange(cv2.cvtColor(img, cv2.COLOR_BGR2HSV), lower_black, upper_black)
    
    
    # mask = cv2.bitwise_not(mask)
    
    # Apply the mask to the original image
    # result = cv2.bitwise_and(img, img, mask=mask)

    # Display the resulting image
    resized = cv2.resize(mask, (int(mask.shape[1]/2), int(mask.shape[0]/4)))
    cv2.imshow('image', resized)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()

# 155 0 64 for pink

# 83 68 63