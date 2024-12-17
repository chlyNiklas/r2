from collections.abc import Sequence
import cv2
import numpy as np
from cv2.typing import MatLike


def main():
    cap = cv2.VideoCapture("video.MP4")

    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret:
            # Display the resulting frame
            # edge = cv2.Canny(frame, 100, 100)
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert to Grayscale
            patches = detect_patches(img, 20)
            # cv2.imshow("patch", patches)

            img = cv2.subtract(img, patches)

            img = cv2.GaussianBlur(img, (5, 5), 0)
            ret, img = cv2.threshold(
                img, 150, 255, cv2.THRESH_BINARY_INV
            )  # apply threshold
            # cv2.imshow("thresh", img)
            blobs = detect_blobs(img)
            print(len(blobs))
            frame = cv2.drawKeypoints(
                frame,
                blobs,
                np.array([]),
                (0, 0, 255),
                cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
            )

            cv2.imshow("Frame", frame)
        else:
            break

        if cv2.waitKey(25) & 0xFF == ord("q"):
            break


def detect_patches(img: MatLike, size: int) -> MatLike:
    img = cv2.GaussianBlur(img, (size * 2 + 1, size * 2 + 1), 0)
    _, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)  # apply threshold
    return img


def detect_blobs(img: MatLike) -> Sequence[cv2.KeyPoint]:
    # Setup SimpleBlobDetector parameters.
    # params = cv2.SimpleBlobDetector_Params()
    params = cv2.SimpleBlobDetector.Params()

    # # Change thresholds
    # params.minThreshold = 100
    # params.maxThreshold = 2000
    # # Filter by Area.
    # params.filterByArea = False
    # params.minArea = 5
    # params.maxArea = 1000

    # # Filter by Circularity
    # params.filterByCircularity = False
    # params.minCircularity = 0.001

    # # Filter by Convexity
    # params.filterByConvexity = False
    # params.minConvexity = 0.87

    # # Filter by Inertia
    # params.filterByInertia = False
    # params.minInertiaRatio = 0.01

    detector = cv2.SimpleBlobDetector.create()
    # Detect blobs.
    return detector.detect(img)

    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob


if __name__ == "__main__":
    main()
