from kivy.uix.boxlayout import BoxLayout

from processor.model import Detector


class SettingsPanel(BoxLayout):
    detector: Detector

    def __init__(self, detector: Detector):
        super().__init__(orientation="vertical")
        self.detector = detector
