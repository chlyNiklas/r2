from typing import Any
import cv2
from kivy.uix.image import Image
from kivymd.uix.button import MDTextButton
from kivymd.uix.gridlayout import MDGridLayout
from processor.model import Detector
from kivy.clock import Clock
from kivymd.uix.menu import MDDropdownMenu


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


class SourceSelector(MDGridLayout):
    menu_items: list[dict[str, Any]] = []
    detector: Detector

    def __init__(self, detector: Detector, **kwargs):
        super().__init__(cols=1, **kwargs)
        self.detector = detector

        self.button = MDTextButton()
        self.button.padding = 10
        self.button.text = "Select Video Source"
        self.button.on_release = lambda: self.dropdown.open()
        self.add_widget(self.button)

        self.assemble_sources()
        self.dropdown = MDDropdownMenu(
            caller=self.button,
            items=self.menu_items,
            width_mult=4,
        )

    def select_source(self, source: VideoSource):
        print(source.name)
        cap = cv2.VideoCapture(source.src)
        self.detector.reset(cap)
        self.dropdown.dismiss()

    def assemble_sources(self):
        sources: list[VideoSource] = []
        for i in range(10):  # maybe check for more cameras (heat, normal, night, tele)
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                sources.append(VideoSource(f"capture: {i}", i))
        sources.append(VideoSource("Original video", "video.mp4"))
        sources.append(VideoSource("Clean test video", "video_clean.mp4"))

        for source in sources:
            print(source.name)
            self.menu_items.append(
                {
                    "viewclass": "OneLineListItem",
                    "text": source.name,
                    "on_release": lambda src=source: self.select_source(src),
                },
            )
