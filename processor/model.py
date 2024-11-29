from datetime import datetime
import base64

from PIL.Image import Image

TIME_FMT = "%d/%m/%y %H:%M:%S.%f"


class Capture:
    coordinates: tuple[float, float]
    time: datetime
    image: Image
    distance: float

    def to_dict(self) -> dict:
        return {
            "coordinates": {"x": self.coordinates[0], "y": self.coordinates[1]},
            "time": self.time.strftime(TIME_FMT),
            "image": base64.b64encode(self.image.tobytes()).decode("utf-8"),
            "distance": self.distance,
        }


class Hit(Capture):
    detected: list[tuple[int, int, float]]  # x, y, radius

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["detected"] = list(
            map(lambda d: {"x": d[0], "y": d[1], "radius": d[2]}, self.detected)
        )
        return d
