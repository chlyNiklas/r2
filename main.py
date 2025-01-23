import cv2
from kivy.core.window import Window
from kivymd.app import MDApp
from components.video import SourceSelector, VideoDisplay
from components.hits import HitList
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

        video_display = VideoDisplay(d)
        video_display.size_hint = (0.9, 0.9)

        source_selector = SourceSelector(d)
        source_selector.size_hint = (0.1, 0.1)
        source_selector.pos_hint = {"center_x": 0.5}

        stream_layout = MDBoxLayout(orientation="vertical", size_hint=(1, 1))
        stream_layout.add_widget(video_display)
        stream_layout.add_widget(source_selector)

        self.add_widget(stream_layout)

        hit_list = HitList(d)
        hit_list.size_hint = (1, 1)
        hit_list.pos_hint = {"center_x": 0, "center_y": 0.5}
        self.add_widget(hit_list)


class R2App(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return MainLayout(
            orientation="horizontal",
            padding=1,
            spacing=1,
            size_hint=(1, 1)
        )


if __name__ == "__main__":
    R2App().run()
