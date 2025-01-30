from typing import Any, Callable
import cv2
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDTextButton
from kivymd.uix.gridlayout import MDGridLayout
from tkinter import filedialog
from components.video import VideoSource
from processor.model import Detector


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

        filechooser = FileChooser(self.select_source)
        self.menu_items.append(filechooser.get_dict())
        self.assemble_sources()
        self.dropdown = MDDropdownMenu(
            caller=self.button,
            items=self.menu_items,
            width_mult=4,
        )

    def select_source(self, source: VideoSource):
        cap = cv2.VideoCapture(source.src)
        self.detector.reset(cap)
        self.dropdown.dismiss()

    def assemble_sources(self):
        sources: list[VideoSource] = []
        for i in range(10):  # maybe check for more cameras (heat, normal, night, tele)
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                sources.append(VideoSource(f"Capture: {i}", i))

        for source in sources:
            self.menu_items.append(
                {
                    "viewclass": "OneLineListItem",
                    "text": source.name,
                    "on_release": lambda src=source: self.select_source(src),
                },
            )

    def file_manager_open(self):
        from tkinter import filedialog

        path = filedialog.askopenfilename()
        # this method returns a list with the first index
        # being the path of the file selected
        print(path)


class FileChooser:
    callback: Callable[[VideoSource], None]

    def __init__(self, callback: Callable[[VideoSource], None]) -> None:
        self.callback = callback

    def get_dict(self) -> dict[str, Any]:
        return {
            "viewclass": "OneLineListItem",
            "text": "Select file",
            "on_release": self.open,
        }

    def open(self):
        try:
            path = filedialog.askopenfilename()
            self.callback(VideoSource("Custom File", path))
        except:
            pass
