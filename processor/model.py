import cv2
import numpy as np
import cvexecutor as cv
from kivy.graphics.texture import Texture


class Detector:
    frame: cv2.typing.MatLike
    cap: cv2.VideoCapture

    def __init__(self, cap: cv2.VideoCapture):
        self.cap = cap

    def getFrame(self) -> Texture:
        buf = self.frame.tobytes()
        image_texture = Texture.create(
            size=(self.frame.shape[1], self.frame.shape[0]), colorfmt="bgr"
        )
        image_texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")
        return image_texture

    def imgShow(self):
        cv2.imshow("Frame", self.frame)

    def process(self):
        if not self.cap.isOpened():
            return

        ret, frame = self.cap.read()

        if not ret:
            return

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert to Grayscale
        # cv2.imshow("1", img)

        cv2.imshow("Frame", img)

        ## remove large patches
        patches = cv.detect_patches(img, 40)
        img = cv2.subtract(img, patches)

        _, img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV)  # apply threshold

        blobs = cv.detect_blobs(img)
        print(len(blobs))
        # frame = cv2.drawKeypoints(
        #     frame,
        #     blobs,
        #     np.array([]),
        #     (0, 0, 255),
        #     cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
        # )
        self.frame = cv.drawKeyPts(frame, blobs, (0, 0, 225))
