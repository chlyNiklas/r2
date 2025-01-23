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
        video_display.size_hint = (1, 1)
        video_display.pos_hint = {"center_x": 1, "center_y": 0.5}
        self.add_widget(video_display)

        source_selector = SourceSelector(d)
        source_selector.size_hint = (0.3, 1)
        source_selector.pos_hint = {"center_x": 0, "center_y": 0.5}
        self.add_widget(source_selector)

        hit_list = HitList(d)
        hit_list.size_hint = (0.3, 1)
        hit_list.pos_hint = {"center_x": 0, "center_y": 0.5}
        self.add_widget(hit_list)

        #self.add_widget(VideoDisplay(d))
        #self.add_widget(SourceSelector(d))
        #self.add_widget(HitList(d))


class R2App(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return MainLayout(
            orientation="horizontal",
            padding=10,
            spacing=10,
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )


if __name__ == "__main__":
    R2App().run()
