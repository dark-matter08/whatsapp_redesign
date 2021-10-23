from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivy.properties import OptionProperty, DictProperty, StringProperty, BooleanProperty
from kivy.lang.builder import Builder
from kivy.uix.textinput import TextInput
from kivymd.uix.label import MDLabel
from functools import partial
from demo.demo import profiles

Builder.load_file('story.kv')
Builder.load_file('chat_list.kv')
Builder.load_file('chat_screen.kv')
Builder.load_file('text_field.kv')
Builder.load_file('chat_bubble.kv')
Window.size = (345, 600)


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

class ChatListItem(RectangularRippleBehavior, MDCard):
    """A clickable row for chats"""
    message = StringProperty()
    friend_avatar = StringProperty()
    friend_name = StringProperty()
    time_stamp = StringProperty()
    status_icon = StringProperty()
    profile = DictProperty()
    is_read = OptionProperty(None, options=['delivered', 'read', 'new', 'waiting', 'sent', 'read_by_me', 'unread'])

# =========== Chat screen classes =============
class ChatScreen(Screen):
    """"A screen that displays chat with a user"""
    text = StringProperty()
    image = StringProperty()
    active_text = StringProperty()
    active = BooleanProperty()

class ChatTextInput(TextInput):
    send_microphone = StringProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_focus(self, instance, value):
        if value:
            # print('User focused', instance)
            pass
        else:
            # print('User defocused', value)
            pass

    def on_text(self, instance, value):
        # print('The widget', instance, 'have:', value)
        text_data = self.text
        send_mic = self.parent.parent.children[0]
        if text_data  == "":
            send_mic.icon = 'microphone'
            # Animation(icon = 'microphone', d=0.4).start(send_mic)
        else:
            send_mic.icon = 'send'
            # Animation(icon = 'send', d=0.4).start(send_mic)

        # try to adjust cursor position

    def set_cursor(self, pos, dt):
        self.cursor = pos

class ChatBubble(MDBoxLayout):
    message = StringProperty()
    time = StringProperty()
    bubble_icon = StringProperty()
    sender = StringProperty()
    is_read = OptionProperty('waiting', options=['delivered', 'read', 'waiting', 'sent'])

class Message(MDLabel):
    """ The addaptiveMessage to be placed in the chat buble"""

class ChatApp(MDApp):
    def build(self):
        # load the kv file
        self.load_kv("main.kv")
        self.story_builder()
        self.chat_list_builder()

        # setting theme properties

        self.theme_cls.primary_palete = 'Teal' #Main color
        self.theme_cls.theme_style = 'Dark' #Dark theme
        # self.theme_cls.theme_style = 'Light' #Light theme
        self.theme_cls.accent_palette = 'Teal'  #Second color with 400 hue value

        self.theme_cls.primary_hue = '400'
        self.theme_cls.primary_dark_hue = '900'
        self.theme_cls.primary_light_hue = '200'
        self.title = 'WhatsApp Redesign'

    def story_builder(self):
        # create story for each user and add to the layout
        story_item = self.root.ids.message_screen.ids.story_layout
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
                last_message, time, is_read, sender, unread = message.split(';')
                icons = {
                    'read': 'checkbox-multiple-marked-circle',
                    'delivered': 'checkbox-multiple-marked-circle-outline',
                    'new':f'numeric-{unread}-circle',
                    'sent':'check-circle-outline',
                    'waiting':'clock-outline'}


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

    def create_chat(self, profile):
        """Get all user messages and create chat bubles"""
        last_seen = "18:00"
        active = profile['active']
        if active:
            active_text = "Online"
        else:
            active_text = f"last seen {last_seen}"

        chat_screen = ChatScreen(
            text = profile['name'],
            image = profile['image'],
            active = active,
            active_text = active_text
        )
        # self.root.add_widget(chat_screen)
        self.message_builder(profile, chat_screen)
        self.root.switch_to(chat_screen)

    def message_builder(self, profile, screen):
        # create message bubles for chat screen
        for messages in profile['msg']:
            if messages != "":
                message, time, is_read, sender, unread = messages.split(';')
                icons = {
                    'read': 'check-bold',
                    'delivered': 'check-all',
                    'sent':'check',
                    'waiting':'clock-outline'}

                bubble_icon = icons[is_read] if is_read in icons.keys() else ''

                chat_bubble = ChatBubble(
                    message = message,
                    time = time,
                    bubble_icon = bubble_icon,
                    sender = sender
                )
                screen.ids.message_history.add_widget(chat_bubble)



ChatApp().run()
