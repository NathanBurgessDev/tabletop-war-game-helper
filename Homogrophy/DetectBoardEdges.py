import cv2 as cv
import imutils
import numpy as np
import math
from matplotlib	import pyplot as plt

def main():
    image = cv.imread("Homogrophy/TopDownLandscape.jpeg")

    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = imutils.resize(image, height = 500)


    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (5, 5), 0)

    # dst = cv.cornerHarris(gray,2,9,0.04)

    # kernel = np.ones((3,3),np.uint8)
    # erosion = cv.erode(gray,kernel,iterations = 10)
    # gray = cv.dilate(erosion,kernel,iterations = 10)

    edged = cv.Canny(gray, 20, 200)


    # cnts = cv.findContours(edged.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    # cnts = imutils.grab_contours(cnts)
    # cnts = sorted(cnts, key = cv.contourArea, reverse = True)[:5]


    # cv.imshow("Outline", gray)
    # cv.imshow("Edged", edged)

    # img = cv.medianBlur(image,5)
    # ret,th1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
    # th2 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C,\
    #             cv.THRESH_BINARY,11,2)
    # th3 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
    #             cv.THRESH_BINARY,11,2)
    # titles = ['Original Image', 'Global Thresholding (v = 127)',
    #             'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
    # images = [img, th1, th2, th3]
    # for i in range(4):
    #     plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
    #     plt.title(titles[i])
    #     plt.xticks([]),plt.yticks([])
    # plt.show()

    cdst = cv.cvtColor(edged, cv.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)

    lines = cv.HoughLines(edged, 1, np.pi / 180, 135, None, 0, 0)

    for line in lines:
            for i in range(0, len(lines)):
                rho = lines[i][0][0]
                theta = lines[i][0][1]
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho
                y0 = b * rho
                pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                cv.line(cdst, pt1, pt2, (0,0,255), 1, cv.LINE_AA)
                print(pt1)
                print(pt2)
                # cv.circle(cdst, pt1, 20, (0,0,255), -1)
                # cv.circle(cdst, pt2, 20, (0,0,255), -1)
 
                
    # lines = []
    # for rho,theta in hLines[0]:
    #     a = np.cos(theta)
    #     b = np.sin(theta)
    #     x0 = a*rho
    #     y0 = b*rho
    #     x1 = int(x0 + 1000*(-b))
    #     y1 = int(y0 + 1000*(a))
    #     x2 = int(x0 - 1000*(-b))
    #     y2 = int(y0 - 1000*(a))
    #     # cv.line(edged, (x1,y1), (x2,y2), (255, 0, 0), 2)
    #     lines.append([[x1,y1],[x2,y2]])
        
    cv.imshow("Lines", cdst)
        

    cv.waitKey(0)
    cv.destroyAllWindows()


# In dissertation discuss using edge and corner detection for board loaction


if __name__ == "__main__":
  main()