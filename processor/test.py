import cv2
from model import Detector


if __name__ == "__main__":
    cap = cv2.VideoCapture("video.mp4")
    # d = Detector(cap)

    # ret, frame = cap.read()

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            cv2.imshow("asdf", frame)
    #     d.process()
    #     d.imgShow()
