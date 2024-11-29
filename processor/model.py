from datetime import datetime
import base64
from io import BytesIO
from PIL import Image

TIME_FMT = "%d/%m/%y %H:%M:%S.%f"


def imagetob64(i: Image.Image) -> str:
    buffered = BytesIO()
    i.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def imagefromb64(b64) -> Image.Image:
    return Image.open(BytesIO(base64.b64decode(b64)))


class Capture:
    coordinates: tuple[float, float]
    time: datetime
    image: Image.Image
    distance: float

    @classmethod
    def from_dict(cls, dict):
        obj = cls()
        obj.coordinates = (dict["coordinates"]["x"], dict["coordinates"]["y"])
        obj.time = datetime.strptime(dict["time"], TIME_FMT)
        obj.image = imagefromb64(dict["image"])
        obj.distance = float(dict["distance"])
        return obj

    def to_hit(self, detected: list[tuple[int, int, float]]):
        h = Hit()
        h.coordinates = self.coordinates
        h.time = self.time
        h.image = self.image
        h.distance = self.distance
        h.detected = detected
        return h

    def to_dict(self) -> dict:
        return {
            "coordinates": {"x": self.coordinates[0], "y": self.coordinates[1]},
            "time": self.time.strftime(TIME_FMT),
            "image": imagetob64(self.image),
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
