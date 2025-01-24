import cv2
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel

from components.video import SourceSelector, VideoDisplay
from components.hits import HitList
from processor.model import Detector
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.card import MDCard
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
        video_display.size_hint = (1, 0.9)

        source_selector = SourceSelector(d)
        source_selector.size_hint = (0.1, 0.1)
        source_selector.pos_hint = {"center_x": 0.5}

        hit_list = HitList(d)
        hit_list.size_hint = (1, 0.95)
        hits_label = MDLabel(text="Hits", halign="center", font_style="H6")
        hits_label.size_hint = (1, 0.05)

        stream_container = MDBoxLayout(orientation="vertical", size_hint=(0.75, 1))

        stream_card = MDCard(
            orientation="vertical",
            size_hint=(1, 1),
            elevation=1,
            radius=[0]
        )

        hits_container = MDBoxLayout(orientation="vertical", size_hint=(0.25, 1))

        hits_card = MDCard(
            orientation="vertical",
            size_hint=(1, 1),
            elevation=1,
            radius=[0]
        )

        stream_card.add_widget(video_display)
        stream_card.add_widget(source_selector)
        stream_container.add_widget(stream_card)

        hits_card.add_widget(hits_label)
        hits_card.add_widget(hit_list)
        hits_container.add_widget(hits_card)

        self.add_widget(stream_container)
        self.add_widget(hits_container)


class R2App(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        return MainLayout(
            orientation="horizontal",
            size_hint=(1, 1)
        )


if __name__ == "__main__":
    R2App().run()
