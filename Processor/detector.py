from model import Hit, Capture
from multiprocessing import Lock


class Resulter:
    def __init__(self):
        self.hits = []

    def get_hits(self, offset=0) -> list[Hit]:
        return self.hits[offset:]

    def register(self, capture: Hit):
        self.hits.append(capture)


class Detector:
    def __init__(self, res: Resulter):
        self.resulter = res
        self.mutex = Lock()

    def calculate(self, capture: Capture):
        pass
