from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivy.properties import OptionProperty, DictProperty, StringProperty, BooleanProperty
from kivy.lang.builder import Builder
from demo.demo import profiles

Builder.load_file('story.kv')
Builder.load_file('chat_list.kv')
Builder.load_file('chat_screen.kv')
Window.size = (365, 600)


# =========== Message Screen classes ==========
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

class ChatListItem(MDCard):
    """A clickable row for chats"""
    message = StringProperty()
    friend_avatar = StringProperty()
    friend_name = StringProperty()
    time_stamp = StringProperty()
    status_icon = StringProperty()
    profile = DictProperty()
    is_read = OptionProperty(None, options=['delivered', 'read', 'new', 'waiting', 'sent'])

# =========== Chat screen classes =============
class ChatScreen(Screen):
    """"A screen that displays chat with a user"""
    text = StringProperty()
    image = StringProperty()
    active = BooleanProperty()

class ChatApp(MDApp):
    def build(self):
        # load the kv file
        self.load_kv("main.kv")
        self.story_builder()
        self.chat_list_builder()

        # setting theme properties

        self.theme_cls.primary_palete = 'Teal' #Main color
        self.theme_cls.theme_style = 'Light' #Dark theme
        # self.theme_cls.accent_color = 'Teal'  #Second color with 400 hue value
        self.theme_cls.accent_hue = '400'
        self.title = 'WhatsApp Redesign'

    def story_builder(self):
        # create story for each user and add to the layout
        story_item = self.root.ids.message_screen.ids.story_layout
        print(story_item)
        for profile in profiles:
            story_item.add_widget(
                StoryWithImage(
                    text = profile['name'],
                    source = profile['image']
                )
            )

    def chat_list_builder(self):
        chat_time_line = self.root.ids.message_screen.ids.chat_time_line
        for profile in profiles:
            for message in profile['msg']:
                last_message, time, is_read, sender = message.split(';')
                icons = {
                    'read': 'checkbox-multiple-marked-circle',
                    'delivered': 'checkbox-multiple-marked-circle-outline',
                    'new':'numeric-1-circle',
                    'sent':'check-circle-outline',
                    'waiting':'dots-horizontal-circle-outline'}
                status_icon = icons[is_read] if is_read in icons.keys() else ''

            chat_time_line.add_widget(
                    ChatListItem(
                        profile = profile,
                        friend_name = profile['name'],
                        friend_avatar = profile['image'],
                        message = last_message,
                        time_stamp = time,
                        is_read = is_read,
                        status_icon = status_icon
                    )
                )


ChatApp().run()
