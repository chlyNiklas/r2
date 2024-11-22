from datetime import datetime

from PIL.Image import Image
from model import Hit
import api
import detector as d


if __name__ == "__main__":
    res = d.Resulter()
    det = d.Detector(res)

    img = Image()
    h = Hit()
    h.coordinates = (500, 5000)
    h.time = datetime.now()
    h.image = img
    h.detected = [(3, 3, 3)]
    h.distance = 5

    res.register(h)
    res.register(h)
    res.register(h)
    res.register(h)
    res.register(h)
    res.register(h)
    api.run(det, res)
