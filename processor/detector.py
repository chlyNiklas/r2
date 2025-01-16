import cv2
import cvexecutor as cv
import multiprocessing as mp
from kivy.graphics.texture import Texture


class Detector:
    frame: cv2.typing.MatLike
    cap: cv2.VideoCapture

    def __init__(self, cap: cv2.VideoCapture):
        self.cap = cap
        p = mp.Process(target=cv.detect, args=[self])
        p.start()

    def getFrame(self) -> Texture:
        buf = self.frame.tobytes()
        image_texture = Texture.create(
            size=(self.frame.shape[1], self.frame.shape[0]), colorfmt="bgr"
        )
        image_texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")
        return self.frame
