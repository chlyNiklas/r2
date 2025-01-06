from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

class MyApp(App):
    def build(self):
        main_layout = FloatLayout()

        # Panel 1: Live Stream
        live_stream_panel = BoxLayout(orientation='vertical', size_hint=(0.5, 0.5), pos_hint={'x': 0, 'y': 0})
        # image feed needs connection to api atm static image for showcase and layout calculation
        live_stream_image = Image(source='IR_7134.jpg', allow_stretch=True, keep_ratio=True)
        live_stream_panel.add_widget(live_stream_image)
        main_layout.add_widget(live_stream_panel)

        # Panel 2: Settings Dropdown
        settings_button = Button(text='Settings', size_hint=(0.2, 0.1), pos_hint={'x': 0.5, 'y': 0.9})
        settings_dropdown = DropDown()
        settings_dropdown.add_widget(Button(text='Setting 1', size_hint_y=None, height=40))
        settings_dropdown.add_widget(Button(text='Setting 2', size_hint_y=None, height=40))
        settings_dropdown.add_widget(Button(text='Setting 3', size_hint_y=None, height=40))
        settings_button.bind(on_release=settings_dropdown.open)
        settings_dropdown.bind(on_select=lambda instance, x: setattr(settings_button, 'text', x))
        main_layout.add_widget(settings_button)

        # Panel 3: Log Stream
        log_stream_panel = ScrollView(size_hint=(0.5, 0.5), pos_hint={'x': 0.5, 'y': 0})
        log_stream_label = Label(text='Log stream data', font_size=20)
        log_stream_panel.add_widget(log_stream_label)
        main_layout.add_widget(log_stream_panel)

        return main_layout


if __name__ == '__main__':
    MyApp().run()
