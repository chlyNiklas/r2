from collections.abc import Sequence
import numpy as np
import cv2
from cv2.typing import MatLike, Scalar


def drawKeyPts(frame: MatLike, keyp, color: Scalar, thickness=3) -> MatLike:
    for curKey in keyp:
        x = int(curKey.pt[0])
        y = int(curKey.pt[1])
        size = int(curKey.size)
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
