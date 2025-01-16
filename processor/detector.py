import cv2
import cvexecutor as cv
import multiprocessing as mp
from kivy.graphics.texture import Texture


class Detector:
    frame: Texture
    cap: cv2.VideoCapture

    def __init__(self, cap: cv2.VideoCapture):
        self.cap = cap
        p = mp.Process(target=cv.detect, args=[self])
        p.start()

    def getFrame(self) -> Texture:
        return self.frame
