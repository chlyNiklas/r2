import cv2 as cv
from cv2.typing import MatLike
import processor.cvlib as cl

from kivy.graphics.texture import Texture

from processor.history import Kitz, Library
from processor.motion import Orienter

COLOR_RED = (0, 0, 225)


class Detector:
    last_frame: MatLike | None = None
    proc_frame: MatLike | None = None
    video_capture: cv.VideoCapture
    coordinator: Orienter
    captures: Library = Library(30)

    def __init__(self, cap: cv.VideoCapture):
        self.video_capture = cap
        self.coordinator = Orienter()

    def reset(self, cap: cv.VideoCapture):
        self.video_capture = cap
        self.coordinator = Orienter()
        self.last_frame = None
        self.proc_frame = None
        self.captures.kitzes = []  # empty all kitzes

    def getFrame(self) -> Texture:
        if self.proc_frame is None:
            return Texture.create()
        return cl.to_texture(self.proc_frame)

    def imgShow(self):
        if self.proc_frame is None:
            return
        cv.imshow("Frame", self.proc_frame)

    def calcMovement(self, frame: MatLike) -> None:
        if self.last_frame is not None:
            self.coordinator.process(self.last_frame, frame)

        self.last_frame = frame

    def process(self):
        if not self.video_capture.isOpened():
            return

        ret, frame = self.video_capture.read()

        if not ret:
            return

        self.captures.clean()

        img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)  # convert to Grayscale

        self.proc_frame = frame

        self.calcMovement(img)

        ## remove large patches
        patches = cl.detect_patches(img, 40)
        img = cv.subtract(img, patches)

        _, img = cv.threshold(img, 200, 255, cv.THRESH_BINARY_INV)  # apply threshold

        blobs = cl.detect_blobs(img)

        for blob in blobs:
            c = (blob.pt[0], blob.pt[1])
            self.captures.register(
                self.coordinator.absolute(c), cl.crop_to(frame, c, 50, 50)
            )

        def kiz_to_cord(kiz: Kitz) -> tuple[float, float]:
            return self.coordinator.relative(kiz.coordinates())

        kizs = map(kiz_to_cord, self.captures.kitzes)

        self.proc_frame = cl.drawKeyPts(
            frame,
            kizs,
            (0, 0, 225),
        )

    def get_kizs(self) -> list[Kitz]:
        return self.captures.kitzes
