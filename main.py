import cv2
from kivy.core.window import Window
from kivymd.app import MDApp
from components.video import SourceSelector, VideoDisplay
from components.hits import HitList, HitList
from processor.model import Detector
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock

Window.size = (1200, 600)
Window.top = 100
Window.left = 200


class MainLayout(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        d = Detector(cv2.VideoCapture())

        Clock.schedule_interval(lambda _: d.process(), 1.0 / 60.0)

        self.add_widget(VideoDisplay(d))
        self.add_widget(SourceSelector(d))
        self.add_widget(HitList(d))


class R2App(MDApp):
    def build(self):
        return MainLayout()


if __name__ == "__main__":
    R2App().run()
