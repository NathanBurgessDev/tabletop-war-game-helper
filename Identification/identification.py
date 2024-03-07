import cv2 as cv
import math

img = cv.imread("Identification/attempt1.png")

redLower = (0, 0, 200)
redUpper = (100, 100, 255)
redFrame = cv.inRange(img, redLower, redUpper)

cnts = cv.findContours(redFrame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

redCenterPoints = []
try:
    for i, c in enumerate(cnts[0]):
        # compute the center of the contour
        M = cv.moments(c)
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        print(f"Red Box {i} : cx={cx}, cy={cy}") 
        cv.circle(redFrame, (cx, cy), 1, (0, 255, 0), 3)
        redCenterPoints.append((cx, cy))
        cv.drawContours(redFrame, [c], -1, (255, 255, 255), 5)
except:
    ()

height, width = img.shape[:2]
center =(width/2, height/2)
rotationMatrix = cv.getRotationMatrix2D(center = center, angle = 18, scale = 1)

# Method 1 
# Get center point of the circle from circle detection# 
# find the red point A  maximum of circle radius + a bit 
# Rotate the image around that center point



print((img[418,347]))
    
print(redCenterPoints[0])

data = []
rotate = img.copy()
for x, y in redCenterPoints:
    print(f"Red Box : x={x}, y={y}")
    newPosX =x * math.cos(math.radians(18)) - y * math.sin(math.radians(18))
    newPosY =x * math.sin(math.radians(18)) + y * math.cos(math.radians(18))
    cv.circle(rotate, (int(newPosX), int(newPosY)), 1, (0, 255, 0), 3)
 

        
print(data)
# resized = cv.resize(redFrame, (int(redFrame.shape[1]/2), int(redFrame.shape[0]/2)))
cv.imshow("circles",redFrame)
cv.imshow("rotate",rotate)
cv.imshow("img",img)


k = cv.waitKey(0)


# There are 2 ways of going round the circle to find the data
# 1. Rotate the image and get the pixel value at the same point
# This requires an accurate center point - and also probably quite slow to do
# 2. Use the equation of the circle to check the points on the image exactly.


# Use circle detection to get center position
# Calculate radius to center of red contour 
# Use circle equation to get the points on the circle


# Talk about using 2 circles instead of 1 - objects next to eachother cuase problems if not using HoughCircles