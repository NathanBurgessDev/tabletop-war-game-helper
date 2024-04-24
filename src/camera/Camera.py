import cv2 as cv

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


