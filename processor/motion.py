from cv2.typing import MatLike
import numpy as np
import cv2 as cv


class Cordinator:
    x: float = 0
    y: float = 0

    def offset(self, x: float, y: float) -> None:
        self.x -= x
        self.y -= y

    def relative(self, rel: tuple[float, float]) -> tuple[float, float]:
        return (rel[0] - self.x, rel[1] - self.y)

    def absolute(self, rel: tuple[float, float]) -> tuple[float, float]:
        return (rel[0] + self.x, rel[1] + self.y)


class Orienter(Cordinator):
    feature_params = dict(
        maxCorners=100, qualityLevel=0.2, minDistance=7, blockSize=7
    )  # Parameters for ShiTomasi corner detection
    lk_params = dict(
        winSize=(15, 15),
        maxLevel=2,
        criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03),
    )  # Parameters for Lucas-Kanade optical flow
    p0: cv.typing.MatLike | None = None
    frame_center: tuple[int, int] | None = None
    max_distance = 600.0  # How far a tracking point can be away from center

    def __init__(
        self, feature_params=dict(), lk_params=dict(), max_distance: float = 600.0
    ) -> None:
        super().__init__()
        self.feature_params = self.feature_params | feature_params
        self.lk_params = self.lk_params | lk_params
        self.max_distance = max_distance

    def process(self, old_frame: MatLike, new_frame: MatLike) -> None:
        ## on first run initialize
        if self.frame_center is None:
            self.frame_center = (new_frame.shape[1] // 2, new_frame.shape[0] // 2)

        if self.p0 is None or len(self.p0) < 10:
            new_points = cv.goodFeaturesToTrack(
                old_frame,
                mask=None,
                **self.feature_params,  # type: ignore[type-var]
            )  # type: ignore[type-var]
            if new_points is not None:
                if self.p0 is not None:
                    self.p0 = np.vstack((self.p0, new_points))
                else:
                    self.p0 = new_points

        p1, st, _ = cv.calcOpticalFlowPyrLK(
            old_frame,
            new_frame,
            self.p0,
            None,
            **self.lk_params,  # type: ignore[type-var]
        )  # type: ignore[type-var]

        # Select valid (tracked) points
        if p1 is not None:
            good_new = p1[st == 1]
            good_old = self.p0[st == 1]  # type: ignore[type-var]

            # Filter points by distance from center
            filtered_new = []
            filtered_old = []
            for new_frame, old_frame in zip(good_new, good_old):
                a, b = new_frame.ravel()
                dist = np.sqrt(
                    (a - self.frame_center[0]) ** 2 + (b - self.frame_center[1]) ** 2
                )

                if dist <= self.max_distance:
                    filtered_new.append(new_frame)
                    filtered_old.append(old_frame)

            # Convert filtered points back to numpy arrays
            good_new = np.array(filtered_new)
            good_old = np.array(filtered_old)

            # get median vector
            xs = []
            ys = []
            for _, (new, old) in enumerate(zip(good_new, good_old)):
                x, y = new.ravel()
                xo, yo = old.ravel()
                xs.append(x - xo)
                ys.append(y - yo)
            self.offset(float(np.median(xs)), float(np.median(ys)))

            # Update points
            self.p0 = good_new.reshape(-1, 1, 2)
