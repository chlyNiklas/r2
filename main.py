import cv2
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Line
from kivy.graphics.texture import Texture
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput

from processor.model import Detector

Window.size = (1200, 600)
Window.top = 100
Window.left = 200


class KivyCamera(Image):
    detector: Detector

    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = cv2.VideoCapture(
            0
        )  # index 0 is default camera, needs to be changed to video stream (link to
        # source selection in settings dropdown
        self.video_sources = self.get_video_sources()
        self.dropdown = DropDown()
        for source in self.video_sources:
            btn = Button(text=source, size_hint_y=None, height=20)
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)
        self.dropdown.bind(on_select=lambda instance, x: self.update_video_source(x))
        self.source_button = Button(
            text="Select Video Source",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"center_x": 0.5, "y": 0.1},
        )
        self.source_button.bind(on_release=self.dropdown.open)
        self.add_widget(self.source_button)
        Clock.schedule_interval(
            self.update_video_stream, 1.0 / 60.0
        )  # per 1.0 seconds update 60 times = 60fps

        self.update_meta_data_callback = None
        self.detector = Detector(cv2.VideoCapture())

    def get_video_sources(self):
        sources = []
        for i in range(3):  # maybe check for more cameras (heat, normal, night, tele)
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                sources.append(f"source {i}")
                cap.release()
                sources.append("mock: video.mp4")
                sources.append("mock: video_o.mp4")
        return sources

    def update_video_source(self, source):
        try:
            index = int(source.split(" ")[1])
            self.detector.cap.release()
            self.detector = Detector(cv2.VideoCapture(index))
        except ValueError:
            index = source.split(" ")[1]
            self.detector.cap.release()
            self.detector = Detector(cv2.VideoCapture(index))

    def update_video_stream(self, dt):
        # extract video stream from video cap
        self.detector.process()
        self.texture = self.detector.getFrame()


class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"

        # Green bordered BoxLayout (Settings panel)
        settings_layout = BoxLayout(orientation="vertical")
        with settings_layout.canvas.before:
            Color(1, 1, 1, 0.5)
            settings_layout.border = Line(
                rectangle=(
                    settings_layout.x,
                    settings_layout.y,
                    settings_layout.width,
                    settings_layout.height,
                ),
                width=2,
            )
            settings_layout.bind(
                pos=self.update_child_border, size=self.update_child_border
            )

        settings_layout.add_widget(Label(text="Settings", font_size=64))
        self.add_widget(settings_layout)

        # Camera View Angle
        camera_view_angle_layout = BoxLayout(orientation="horizontal")
        camera_view_angle_layout.add_widget(
            Label(text="Camera View Angle in Degrees:", font_size=32)
        )
        self.camera_view_angle_input = TextInput(font_size=32, size_hint=(0.25, 0.5))
        camera_view_angle_layout.add_widget(self.camera_view_angle_input)
        settings_layout.add_widget(camera_view_angle_layout)

        # Flight height
        flight_height_layout = BoxLayout(orientation="horizontal")
        flight_height_layout.add_widget(
            Label(text="Flight Height in Meters:", font_size=32)
        )
        self.flight_height_input = TextInput(font_size=32, size_hint=(0.25, 0.5))
        flight_height_layout.add_widget(self.flight_height_input)
        settings_layout.add_widget(flight_height_layout)

        # Kitz Temperature Range
        kitz_temp_layout = BoxLayout(orientation="horizontal")
        kitz_temp_layout.add_widget(Label(text="Kitz Temperature Range:", font_size=32))
        self.kitz_temp_slider = Slider(min=0, max=100, value=50, size_hint=(0.5, 1))
        self.kitz_temp_label = Label(text="50", font_size=32)
        self.kitz_temp_slider.bind(value=self.update_kitz_temp_label)
        kitz_temp_layout.add_widget(self.kitz_temp_slider)
        kitz_temp_layout.add_widget(self.kitz_temp_label)
        settings_layout.add_widget(kitz_temp_layout)

        # Camera Temperature
        camera_temp_layout = BoxLayout(orientation="horizontal")
        camera_temp_layout.add_widget(Label(text="Camera Temperature:", font_size=32))
        self.camera_temp_slider = Slider(min=0, max=100, value=50, size_hint=(0.5, 1))
        self.camera_temp_label = Label(text="50", font_size=32)
        self.camera_temp_slider.bind(value=self.update_camera_temp_label)
        camera_temp_layout.add_widget(self.camera_temp_slider)
        camera_temp_layout.add_widget(self.camera_temp_label)
        settings_layout.add_widget(camera_temp_layout)

        # (Hits panel)
        hits_anchor = AnchorLayout(anchor_y="top", size_hint_x=None, width=150)
        with hits_anchor.canvas.before:
            Color(1, 1, 1, 0.5)
            hits_anchor.border = Line(
                rectangle=(
                    hits_anchor.x,
                    hits_anchor.y,
                    hits_anchor.width,
                    hits_anchor.height,
                ),
                width=2,
            )
            hits_anchor.bind(
                pos=self.update_child_border, size=self.update_child_border
            )

        hits_box = BoxLayout(orientation="vertical", size_hint=(1, None), spacing=100)
        hits_box.bind(
            minimum_height=hits_box.setter("height")
        )  # Dynamically adjust height based on content

        hits_labels = ["", "hits", "hit 1", "hit 2", "hit 3"]

        for text in hits_labels:
            hits_box.add_widget(
                Label(text=text, font_size=48 if text == "hits" else 24)
            )

        hits_anchor.add_widget(hits_box)
        self.add_widget(hits_anchor)

        # (Video and Metadata panel)
        stream_layout = BoxLayout(
            orientation="vertical", size_hint=(1, 1), pos_hint={"x": 0, "y": 0}
        )

        with stream_layout.canvas.before:
            Color(1, 1, 1, 0.5)
            stream_layout.border = Line(
                rectangle=(
                    stream_layout.x,
                    stream_layout.y,
                    stream_layout.width,
                    stream_layout.height,
                ),
                width=2,
            )
            stream_layout.bind(
                pos=self.update_child_border, size=self.update_child_border
            )
        self.camera_widget = KivyCamera(size_hint=(1, 1), pos_hint={"x": 0, "y": 0})
        self.meta_data_label = Label(text="Meta Data:", font_size=40)
        stream_layout.add_widget(self.camera_widget)
        stream_layout.add_widget(self.meta_data_label)
        self.add_widget(stream_layout)

    def update_meta_data_label(self, meta_data):
        self.meta_data_label.text = f"Meta Data: {meta_data}"

    def update_kitz_temp_label(self, instance, value):
        self.kitz_temp_label.text = str(int(value))

    def update_camera_temp_label(self, instance, value):
        self.camera_temp_label.text = str(int(value))

    def update_border(self, *args):
        self.border.rectangle = (self.x, self.y, self.width, self.height)

    def update_child_border(self, instance, *args):
        instance.border.rectangle = (
            instance.x,
            instance.y,
            instance.width,
            instance.height,
        )


class MyApp(App):
    def build(self):
        return MyBoxLayout()


if __name__ == "__main__":
    MyApp().run()
    # CameraApp().run()
