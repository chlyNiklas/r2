import cv2 as cv
from cv2.typing import MatLike
import numpy as np
import processor.cvlib as cl

from kivy.graphics.texture import Texture

# params for ShiTomasi corner detection
feature_params = dict(
    maxCorners=100,
    qualityLevel=0.3,
    minDistance=7,
)

# Parameters for lucas kanade optical flow
lk_params = dict(
    winSize=(15, 15),
    maxLevel=2,
    criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03),
)


class Cordinator:
    x: float = 0
    y: float = 0

    def offset(self, x: float, y: float) -> None:
        self.x += x
        self.y += y
        print(x, self.x, y, self.y)

    def relative(self, rel: tuple[float, float]) -> tuple[float, float]:
        return (rel[0] + self.x, rel[1] + self.y)

    def absolute(self, rel: tuple[float, float]) -> tuple[float, float]:
        return (rel[0] + self.x, rel[1] + self.y)


class Detector:
    last_frame: MatLike | None = None
    proc_frame: MatLike | None = None
    cap: cv.VideoCapture
    cord: Cordinator

    def __init__(self, cap: cv.VideoCapture):
        self.cap = cap
        self.cord = Cordinator()

    def getFrame(self) -> Texture:
        if self.proc_frame is None:
            return Texture.create()
        buf = self.proc_frame.tobytes()
        image_texture = Texture.create(
            size=(self.proc_frame.shape[1], self.proc_frame.shape[0]), colorfmt="bgr"
        )
        image_texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")
        return image_texture

    def imgShow(self):
        if self.proc_frame is None:
            return
        cv.imshow("Frame", self.proc_frame)

    def calcMovement(self, frame: MatLike) -> None:
        frame = cv.resize(frame, None, None, 0.5, 0.5, cv.INTER_CUBIC)
        if self.last_frame is None:
            self.last_frame = frame
            return

        try:
            flow = cv.calcOpticalFlowFarneback(
                self.last_frame, frame, None, 0.5, 3, 15, 3, 5, 1.2, 0
            )
            x = np.median(flow[..., 0]) * 2
            y = np.median(flow[..., 1]) * 2
            self.cord.offset(x, y)
        except cv.error as e:
            print(e)
        except IndexError:
            pass

        self.last_frame = frame

    def process(self):
        if not self.cap.isOpened():
            return

        ret, frame = self.cap.read()

        if not ret:
            return

        img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)  # convert to Grayscale

        self.proc_frame = frame

        self.calcMovement(img)

        ## remove large patches
        patches = cl.detect_patches(img, 40)
        img = cv.subtract(img, patches)

        _, img = cv.threshold(img, 200, 255, cv.THRESH_BINARY_INV)  # apply threshold

        blobs = cl.detect_blobs(img)
        zs = self.cord.relative((500, 500))
        cv.circle(
            frame,
            (int(zs[0]), int(zs[1])),
            11,
            (0, 225, 0),
            thickness=3,
            lineType=8,
            shift=0,
        )

        self.proc_frame = cl.drawKeyPts(frame, blobs, (0, 0, 225))
