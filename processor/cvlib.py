from collections.abc import Sequence
from kivy.uix.textinput import Texture
import numpy as np
import cv2
from cv2.typing import MatLike, Scalar
from typing import Iterable


def drawKeyPts(
    frame: MatLike,
    keyp: Iterable[tuple[float, float]],
    color: Scalar,
    thickness=3,
    size=10,
) -> MatLike:
    for curKey in keyp:
        x = int(curKey[0])
        y = int(curKey[1])
        cv2.circle(
            frame, (x, y), size * 2, color, thickness=thickness, lineType=8, shift=0
        )
    return frame


def detect_patches(img: MatLike, size: int) -> MatLike:
    img = cv2.GaussianBlur(img, (size * 2 + 1, size * 2 + 1), 0)
    _, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)  # apply threshold
    img = cv2.dilate(img, np.ones((11, 11), np.uint8), iterations=3)
    return img


def detect_blobs(img: MatLike) -> Sequence[cv2.KeyPoint]:
    # Setup SimpleBlobDetector parameters.
    # params = cv2.SimpleBlobDetector_Params()
    params = cv2.SimpleBlobDetector.Params()

    detector = cv2.SimpleBlobDetector.create()
    # Detect blobs.
    return detector.detect(img)

    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob


def to_texture(img: MatLike) -> Texture:
    buf = img.tobytes()
    image_texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt="bgr")
    image_texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")
    return image_texture


def crop_to(
    img: MatLike, center: tuple[float, float], height: int, width: int
) -> MatLike:
    h, w = img.shape[:2]
    min_y = max(int(center[1] - height / 2), 0)
    max_y = min(int(center[1] + height / 2), h)
    min_x = max(int(center[0] - width / 2), 0)
    max_x = min(int(center[0] + width / 2), w)

    return img[min_y:max_y, min_x:max_x]
