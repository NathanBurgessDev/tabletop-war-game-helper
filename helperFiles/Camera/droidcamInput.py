import numpy as np
import cv2 as cv
import glob

def main():

    # Use -1 to get a list of available devices
    # for camera in glob.glob("/dev/video?"):
    #     print(camera)
    #     c = cv.VideoCapture(camera)
    # sudo modprobe v4l2loopback
    c = cv.VideoCapture("/dev/video2")
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

class Camera:
    def __init__(self, cameraNumber: int):
        self.camera = cv.VideoCapture("/dev/video"+str(cameraNumber))
        self.camera.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
        self.camera.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
    
    def getFrame(self):
        ret, frame = self.camera.read()
        return frame

    def release(self):
        self.camera.release()




if __name__ == "__main__":
    main()