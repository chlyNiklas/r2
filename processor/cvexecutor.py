from collections.abc import Sequence
from detector import Detector
import numpy as np
import cv2
from cv2.typing import MatLike


def detect(detector: Detector):
    while detector.cap.isOpened():
        # Capture frame-by-frame
        ret, frame = detector.cap.read()
        if ret:
            # Display the resulting frame
            # edge = cv2.Canny(frame, 100, 100)
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert to Grayscale
            # cv2.imshow("1", img)

            ## remove large patches
            patches = detect_patches(img, 40)
            # cv2.imshow("4", patches)
            img = cv2.subtract(img, patches)
            cv2.imshow("adsf", img)

            # img = cv2.GaussianBlur(img, (5, 5), 0)
            # cv2.imshow("2", img)

            ret, img = cv2.threshold(
                img, 200, 255, cv2.THRESH_BINARY_INV
            )  # apply threshold
            cv2.imshow("3", img)

            blobs = detect_blobs(img)
            print(len(blobs))
            # frame = cv2.drawKeypoints(
            #     frame,
            #     blobs,
            #     np.array([]),
            #     (0, 0, 255),
            #     cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
            # )
            frame = drawKeyPts(frame, blobs, (0, 0, 225), 2)

            detector.frame = frame
            cv2.imshow("Frame", frame)
        else:
            break

        if cv2.waitKey(25) & 0xFF == ord("q"):
            break


def drawKeyPts(im, keyp, col, th):
    for curKey in keyp:
        x = int(curKey.pt[0])
        y = int(curKey.pt[1])
        size = int(curKey.size)
        cv2.circle(im, (x, y), size * 2, col, thickness=th, lineType=8, shift=0)
    return im


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
