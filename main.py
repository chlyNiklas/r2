import cv2
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Line
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

Window.size = (1200, 600)
Window.top = 100
Window.left = 200


class KivyCamera(Image):
    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = cv2.VideoCapture(0)  # index 0 is default camera, needs to be changed to video stream (link to
        # source selection in settings dropdown
        self.video_sources = self.get_video_sources()
        self.dropdown = DropDown()
        for source in self.video_sources:
            btn = Button(text=source, size_hint_y=None, height=20)
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)
        self.dropdown.bind(on_select=lambda instance, x: self.update_video_source(x))
        Clock.schedule_interval(self.update, 1.0 / 60.0)  # per 1.0 seconds update 60 times = 60fps

    def get_video_sources(self):
        sources = []
        for i in range(3):  # maybe check for more cameras (heat, normal, night, tele)
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                sources.append(f"source {i}")
                cap.release()
        return sources

    def update_video_source(self, source):
        index = int(source.split(" ")[1])
        self.capture.release()
        self.capture = cv2.VideoCapture(index)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            buf = cv2.flip(frame, 0).tobytes()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = image_texture


class CameraApp(App):
    def build(self):
        return KivyCamera()


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
            Line(rectangle=(settings_layout.x, settings_layout.y, settings_layout.width, settings_layout.height),
                 width=2)

        settings_labels = [
            "Settings",
            "Camera View Angle    °",
            "Flight height    m",
            "Kitz Temperature Range",
            "Camera Temperature",
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
            Line(rectangle=(video_metadata_layout.x, video_metadata_layout.y, video_metadata_layout.width,
                            video_metadata_layout.height), width=2)

        video_metadata_labels = ["img / video flow", "Metadata"]

        for text in video_metadata_labels:
            video_metadata_layout.add_widget(Label(text=text, font_size=64))

        self.add_widget(video_metadata_layout)

        stream_layout = BoxLayout(orientation="vertical", size_hint=(0.5, 0.5), pos_hint={'x': 0, 'y': 0})
        self.camera_widget = KivyCamera(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        stream_layout.add_widget(self.camera_widget)
        self.add_widget(stream_layout)


class MyApp(App):
    def build(self):
        return MyBoxLayout()


if __name__ == "__main__":
    MyApp().run()
    # CameraApp().run()
