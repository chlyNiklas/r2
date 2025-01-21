import math
import processor.cvlib as cl
from kivy.uix.textinput import Texture
import time as t

from cv2.typing import MatLike


class Kitz:
    x: float
    y: float
    dev: float = 0
    updated_num: int = 1
    last_update: float
    image: MatLike | None = None

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.last_update = t.time()

    def update(self, x: float, y: float) -> None:
        d = self.distance(x, y)
        self.dev = (self.dev * self.updated_num + d) / (self.updated_num + 1)

        self.x, self.y = x, y

        self.updated_num += 1
        self.last_update = t.time()

    def distance(self, x: float, y: float) -> float:
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def coordinates(self) -> tuple[float, float]:
        return (self.x, self.y)

    def get_texture(self) -> Texture:
        if self.image is None:
            return Texture()
        return cl.to_texture(Texture)


class Library:
    max_dist: float
    kitzes: list[Kitz] = []

    def __init__(self, max_dist: float) -> None:
        self.max_dist = max_dist

    def register(self, cord: tuple[float, float]) -> None:
        x = round(cord[0])
        y = round(cord[1])
        for kiz in self.kitzes:
            if kiz.distance(x, y) <= self.max_dist:
                kiz.update(x, y)
                return

        self.kitzes.append(Kitz(x, y))

    def clean(self) -> None:
        def isGood(k: Kitz) -> bool:
            ok = k.last_update + 1 > t.time() or k.updated_num > 40
            return ok

        self.kitzes = list(filter(isGood, self.kitzes))
