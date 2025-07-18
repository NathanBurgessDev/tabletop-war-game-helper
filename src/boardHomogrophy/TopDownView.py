import cv2 as cv
import numpy as np
from numpy import ndarray
import path
import sys

direction = path.Path(__file__).abspath()
sys.path.append(direction.parent.parent)

from boardHomogrophy.HomographyUtils import four_point_transform


# import sys
# path_root = Path(__file__).parents[2]
# print(path_root)
# sys.path.append(str(path_root) + "/Diss")
from boardHomogrophy.BoardFinding import getFourCornersCoordinates



# load the image and grab the source coordinates (i.e. the list of
# of (x, y) points)
# NOTE: using the 'eval' function is bad form, but for this example
# let's just roll with it -- in future posts I'll show you how to
# automatically determine the coordinates without pre-supplying them

def calibrateTopDownView(image: ndarray) -> tuple[ndarray,ndarray]:
    pts = getFourCornersCoordinates(image)
    pts = np.array(pts, dtype = "float32")

    return pts
  

def getTopDownView(image: ndarray, pts: ndarray) -> ndarray:
    # # apply the four point tranform to obtain a "birds eye view" of
    # # the image

    warped = four_point_transform(image, pts)
    
    return warped



