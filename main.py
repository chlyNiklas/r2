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
        Clock.schedule_interval(self.update_video_stream, 1.0 / 60.0)  # per 1.0 seconds update 60 times = 60fps

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

    def update_video_stream(self, dt):
        # extract video stream from video cap
        ret, frame = self.capture.read()
        if ret:
            # convert to kivy texture
            buf = cv2.flip(frame, 0).tobytes()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = image_texture

    def update_meta_data(self):
        meta_data = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.meta_data_label.text = f'Meta Data: {meta_data}'
        Clock.schedule_once(self.update_meta_data, 1.0)


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
            self.border = Line(rectangle=(self.x, self.y, self.width, self.height), width=2)
        self.bind(pos=self.update_border, size=self.update_border)

        # Green bordered BoxLayout (Settings panel)
        settings_layout = BoxLayout(orientation="vertical")
        with settings_layout.canvas.before:
            Color(0, 1, 0, 1)  # Green color
            settings_layout.border = Line(
                rectangle=(settings_layout.x, settings_layout.y, settings_layout.width, settings_layout.height),
                width=2)
        settings_layout.bind(pos=self.update_child_border, size=self.update_child_border)

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
            hits_anchor.border = Line(rectangle=(hits_anchor.x, hits_anchor.y, hits_anchor.width, hits_anchor.height),
                                      width=2)
        hits_anchor.bind(pos=self.update_child_border, size=self.update_child_border)

        hits_box = BoxLayout(orientation="vertical", size_hint=(1, None), spacing=100)
        hits_box.bind(minimum_height=hits_box.setter('height'))  # Dynamically adjust height based on content

        hits_labels = ["", "hits", "hit 1", "hit 2", "hit 3"]

        for text in hits_labels:
            hits_box.add_widget(Label(text=text, font_size=48 if text == "hits" else 24))

        hits_anchor.add_widget(hits_box)
        self.add_widget(hits_anchor)

        # Yellow bordered BoxLayout (Video and Metadata panel)
        stream_layout = BoxLayout(orientation="vertical", size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        with stream_layout.canvas.before:
            Color(1, 1, 0, 1)
            stream_layout.border = Line(rectangle=(stream_layout.x, stream_layout.y, stream_layout.width,
                                                   stream_layout.height), width=2)
            stream_layout.bind(pos=self.update_child_border, size=self.update_child_border)
        self.camera_widget = KivyCamera(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        self.meta_data_label = Label(text='Meta Data:', font_size=40)
        stream_layout.add_widget(self.camera_widget)
        stream_layout.add_widget(self.meta_data_label)
        self.add_widget(stream_layout)

    def update_border(self, *args):
        self.border.rectangle = (self.x, self.y, self.width, self.height)

    def update_child_border(self, instance, *args):
        instance.border.rectangle = (instance.x, instance.y, instance.width, instance.height)


class MyApp(App):
    def build(self):
        return MyBoxLayout()


if __name__ == "__main__":
    MyApp().run()
