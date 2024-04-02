import numpy as np
import cv2 as cv
import glob

def main():

    # for camera in glob.glob("/dev/video?"):
    #     print(camera)
    #     c = cv.VideoCapture(camera)
    c = cv.VideoCapture("/dev/video0")
    c.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
    c.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
    while True:
        ret, frame = c.read()
        # print(frame.shape)
        if not ret:
            break
        cv.imshow("frame", frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()