from tkinter import Widget

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

from kivy.core.window import Window
Window.size = (1200, 600)
Window.top = 100
Window.left = 200

class MyBoxLayout(BoxLayout):
    pass

class MyApp(App):
    def build(self):
        return MyBoxLayout()

if __name__ == "__main__":
    MyApp().run()
