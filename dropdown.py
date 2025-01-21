from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown 
class SimpleApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical')
        button = Button(text="Select Video Source", size_hint=(None, None), size=(200, 50))
        dropdown = DropDown()

        for i in range(5):
            btn = Button(text=f'Option {i}', size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

        button.bind(on_release=dropdown.open)
        root.add_widget(button)
        return root

if __name__ == "__main__":
    SimpleApp().run()
