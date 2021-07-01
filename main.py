from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from kivy.lang.builder import Builder
from demo import demo

Builder.load_file('story.kv')
Window.size = (365, 600)


class MessageScreen(Screen):
    """A Screen that display all stories and message history"""

class StoryWithImage(MDBoxLayout):
    """A horizontal layout with the user dp and the username"""
    text = StringProperty()
    source = StringProperty()

class StoryWithIcon(MDBoxLayout):
    """A horizontal layout with the user dp and the username"""
    text = StringProperty()
    icon = StringProperty()

class ChatApp(MDApp):
    def build(self):
        # load the kv file
        self.load_kv("main.kv")

        # setting theme properties
        self.theme_cls.primary_palete = 'Teal' #Main color
        self.theme_cls.theme_style = 'Dark' #Dark theme
        self.theme_cls.accent_color  #Second color with 400 hue value
        self.theme_cls.accent_hue = '400'
        self.title = 'WhatsApp Redesign'




ChatApp().run()
