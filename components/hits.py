from typing import Any
from kivy.core import text
from kivy.uix.image import Image
from kivy.uix.recycleview import ScrollView
from kivymd.uix.label.label import MDLabel
from kivymd.uix.gridlayout import GridLayout
from kivymd.uix.list import (
    MDList,
    OneLineListItem,
)
from kivy.clock import Clock

from processor.model import Detector


class HitList(ScrollView):
    items: list[Any] = []
    detector: Detector

    def __init__(self, d: Detector, **kwargs):
        super().__init__(**kwargs)
        self.detector = d

        self.list_view = MDList()
        self.list_view.row_default_height = 50

        self.add_widget(self.list_view)
        Clock.schedule_interval(
            self.update_list, 1.0 / 10.0
        )  # per 1.0 seconds update 60 times = 60fps

    def clear(self):
        for item in self.items:
            self.list_view.remove_widget(item)
        self.items = []

    def update_list(self, _):
        self.clear()

        for kitz in self.detector.get_kizs():
            item = GridLayout(rows=1)
            item.add_widget(OneLineListItem(text=f"Kitz @ x: {kitz.x} y: {kitz.y}"))
            img = Image()
            img.texture = kitz.get_texture()
            item.add_widget(img)

            self.items.append(item)

        for item in self.items:
            self.list_view.add_widget(item)
