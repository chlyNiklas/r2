from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Line

from kivy.core.window import Window
Window.size = (1200, 600)
Window.top = 100
Window.left = 200

class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"

        # Add red border
        with self.canvas.before:
            Color(1, 0, 0, 1)  # Red color
            Line(rectangle=(self.x, self.y, self.width, self.height), width=2)

        # Green bordered BoxLayout (Settings panel)
        settings_layout = BoxLayout(orientation="vertical")
        with settings_layout.canvas.before:
            Color(0, 1, 0, 1)  # Green color
            Line(rectangle=(settings_layout.x, settings_layout.y, settings_layout.width, settings_layout.height), width=2)

        settings_labels = [
            "Settings",
            "Camera View Angle    °",
            "Fleight height    m",
            "Kitz Temparatur Range",
            "Camera Temparatur",
            "Video Source    ^"
        ]

        for text in settings_labels:
            settings_layout.add_widget(Label(text=text, font_size=32 if text != "Settings" else 64))

        self.add_widget(settings_layout)

        # Blue bordered AnchorLayout (Hits panel)
        hits_anchor = AnchorLayout(anchor_y="top", size_hint_x=None, width=150)
        with hits_anchor.canvas.before:
            Color(0, 0, 1, 1)  # Blue color
            Line(rectangle=(hits_anchor.x, hits_anchor.y, hits_anchor.width, hits_anchor.height), width=2)

        hits_box = BoxLayout(orientation="vertical", size_hint=(None, None), width=150)
        hits_box.height = hits_box.minimum_height
        hits_box.spacing = 50

        hits_labels = ["hits", "hit 1", "hit 2", "hit 3"]

        for text in hits_labels:
            hits_box.add_widget(Label(text=text, font_size=48 if text == "hits" else 24))

        hits_anchor.add_widget(hits_box)
        self.add_widget(hits_anchor)

        # Yellow bordered BoxLayout (Video and Metadata panel)
        video_metadata_layout = BoxLayout(orientation="vertical")
        with video_metadata_layout.canvas.before:
            Color(1, 1, 0, 1)  # Yellow color
            Line(rectangle=(video_metadata_layout.x, video_metadata_layout.y, video_metadata_layout.width, video_metadata_layout.height), width=2)

        video_metadata_labels = ["img / video flow", "Metadata"]

        for text in video_metadata_labels:
            video_metadata_layout.add_widget(Label(text=text, font_size=64))

        self.add_widget(video_metadata_layout)

class MyApp(App):
    def build(self):
        return MyBoxLayout()

if __name__ == "__main__":
    MyApp().run()
