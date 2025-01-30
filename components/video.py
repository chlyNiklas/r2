from kivy.uix.image import Image
from processor.model import Detector
from kivy.clock import Clock


class VideoDisplay(Image):
    detector: Detector

    def __init__(self, detector: Detector, **kwargs):
        super(VideoDisplay, self).__init__(**kwargs)
        self.detector = detector
        Clock.schedule_interval(
            self.update_video_stream, 1.0 / 60.0
        )  # per 1.0 seconds update 60 times = 60fps

    def update_video_stream(self, _):
        # extract video stream from video cap
        self.texture = self.detector.getFrame()


class VideoSource:
    name: str
    src: str | int

    def __init__(self, name: str, src: str | int) -> None:
        self.name = name
        self.src = src
