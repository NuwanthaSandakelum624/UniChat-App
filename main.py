import requests
import json
import os
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ListProperty
from kivy.uix.image import Image
from kivymd.uix.fitimage import FitImage
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDTextButton, MDIconButton
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.video import Video
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock
from plyer import filechooser

Window.size = (360, 640)

FIREBASE_URL = "https://university-app-92c79-default-rtdb.firebaseio.com/"
DEFAULT_AVATAR = "https://cdn-icons-png.flaticon.com/512/149/149071.png"

class ClickableImage(ButtonBehavior, Image):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.is_double_tap:
                MDApp.get_running_app().toggle_zoom_image(self.source)
                return True
        return super().on_touch_down(touch)

class HomeAvatar(FitImage):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            MDApp.get_running_app().go_to_profile()
            return True
        return super().on_touch_down(touch)

class UniChatVideo(RelativeLayout):
    def __init__(self, source, auto_play=False, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 1)

        initial_state = 'play' if auto_play else 'pause'
        self.video = Video(source=source, state=initial_state, options={'eos': 'loop'}, allow_stretch=True,
                           keep_ratio=True)
        self.add_widget(self.video)

        self.controls = MDBoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height="36dp",
            md_bg_color=[0, 0, 0, 0.6],
            padding=[10, 0, 10, 0],
            pos_hint={"x": 0, "y": 0}
        )

        initial_icon = "pause" if auto_play else "play"
        self.play_btn = MDIconButton(
            icon=initial_icon,
            theme_icon_color="Custom",
            icon_color=[1, 1, 1, 1],
            icon_size="18dp",
            pos_hint={"center_y": 0.5}
        )
        self.play_btn.bind(on_release=self.toggle_play)
        self.controls.add_widget(self.play_btn)

        self.v_lbl = MDLabel(text="UniPlayer 🎥", font_style="Caption", theme_text_color="Custom",
                             text_color=[1, 1, 1, 1], pos_hint={"center_y": 0.5})
        self.controls.add_widget(self.v_lbl)

        self.add_widget(self.controls)

        self.hide_clock = None
        if auto_play:
            self.hide_clock = Clock.schedule_once(self.hide_controls, 2.5)
        else:
            self.controls.opacity = 1
            self.controls.disabled = False

    def toggle_play(self, instance):
        if self.video.state == 'play':
            self.video.state = 'pause'
            self.play_btn.icon = "play"
            if self.hide_clock: self.hide_clock.cancel()
            self.show_controls()
        else:
            self.video.state = 'play'
            self.play_btn.icon = "pause"
            self.reset_hide_clock()

    def hide_controls(self, dt=None):
        self.controls.opacity = 0
        self.controls.disabled = True

    def show_controls(self):
        self.controls.opacity = 1
        self.controls.disabled = False
        self.reset_hide_clock()

    def reset_hide_clock(self):
        if self.hide_clock: self.hide_clock.cancel()
        if self.video.state == 'play':
            self.hide_clock = Clock.schedule_once(self.hide_controls, 2.5)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            local_pos = self.to_local(*touch.pos)
            if self.controls.collide_point(*local_pos) and self.controls.opacity == 1:
                return super().on_touch_down(touch)

            if self.controls.opacity == 0:
                self.show_controls()
            else:
                self.controls.opacity = 0
                self.controls.disabled = True
                if self.hide_clock: self.hide_clock.cancel()
            return True
        return super().on_touch_down(touch)


KV = '''
ScreenManager:
    LoginScreen:
    RegisterScreen:
    HomeScreen:
    ProfileScreen:
    OtherProfileScreen:
    CommentScreen:
    ChatScreen:
    ChatListScreen:
    AddPostScreen:
    ZoomScreen:

<LoginScreen>:
    name: "login"
    MDBoxLayout:
        orientation: "vertical"
        padding: 25
        spacing: 18
        md_bg_color: [0.96, 0.97, 0.99, 1]

        Widget:
            size_hint_y: None
            height: "50dp"
        MDLabel:
            text: "UniChat"
            halign: "center"
            font_style: "H3"
            bold: True
            theme_text_color: "Custom"
            text_color: [0.05, 0.45, 0.93, 1]
        MDLabel:
            text: "Log in to connect with your campus friends."
            halign: "center"
            font_style: "Body2"
            theme_text_color: "Secondary"
        Widget:
            size_hint_y: None
            height: "20dp"

        MDTextField:
            id: login_username
            hint_text: "Username"
            mode: "rectangle"
        MDTextField:
            id: login_password
            hint_text: "Password"
            mode: "rectangle"
            password: True

        MDRaisedButton:
            text: "LOG IN"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 1
            height: "50dp"
            md_bg_color: [0.05, 0.45, 0.93, 1]
            on_release: app.process_login()

        MDTextButton:
            text: "Don't have an account? Register here"
            pos_hint: {"center_x": 0.5}
            theme_text_color: "Custom"
            text_color: [0.05, 0.45, 0.93, 1]
            on_release: app.root.current = "register"
        Widget:

<RegisterScreen>:
    name: "register"
    MDBoxLayout:
        orientation: "vertical"
        padding: 25
        spacing: 18
        md_bg_color: [0.96, 0.97, 0.99, 1]

        Widget:
            size_hint_y: None
            height: "40dp"
        MDLabel:
            text: "Create Account"
            halign: "center"
            font_style: "H4"
            bold: True
            theme_text_color: "Custom"
            text_color: [0.05, 0.45, 0.93, 1]
        Widget:
            size_hint_y: None
            height: "10dp"

        MDTextField:
            id: reg_username
            hint_text: "Username"
            mode: "rectangle"
        MDTextField:
            id: reg_email
            hint_text: "Email Address"
            mode: "rectangle"
        MDTextField:
            id: reg_password
            hint_text: "Password"
            mode: "rectangle"
            password: True

        MDRaisedButton:
            text: "REGISTER NOW"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 1
            height: "50dp"
            md_bg_color: [0.05, 0.45, 0.93, 1]
            on_release: app.process_registration()

        MDTextButton:
            text: "Already have an account? Log In"
            pos_hint: {"center_x": 0.5}
            theme_text_color: "Custom"
            text_color: [0.3, 0.3, 0.3, 1]
            on_release: app.root.current = "login"
        Widget:

<HomeScreen>:
    name: "home"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: [0.93, 0.94, 0.96, 1]

        MDBoxLayout:
            size_hint_y: None
            height: "60dp"
            md_bg_color: [1, 1, 1, 1]
            padding: [12, 0, 12, 0]
            spacing: 8

            MDLabel:
                text: "UniChat"
                bold: True
                font_style: "H6"
                size_hint_x: None
                width: "75dp"
                theme_text_color: "Custom"
                text_color: [0.05, 0.45, 0.93, 1]

            MDTextField:
                id: search_input
                hint_text: "Search users..."
                mode: "line"
                size_hint_x: 0.5
                pos_hint: {"center_y": 0.5}
                on_text: app.filter_users(self.text)

            MDIconButton:
                icon: "message-text-outline"
                theme_icon_color: "Custom"
                icon_color: [0.1, 0.1, 0.1, 1]
                pos_hint: {"center_y": 0.5}
                icon_size: "24dp"
                on_release: app.go_to_chat_list()

            HomeAvatar:
                id: home_profile_avatar
                source: "image"
                size_hint: None, None
                size: ["38dp", "38dp"]
                radius: [19, 19, 19, 19]
                pos_hint: {"center_y": 0.5}

        ScrollView:
            id: search_results_scroll
            size_hint_y: None
            height: "0dp"
            canvas.before:
                Color:
                    rgba: [1, 1, 1, 1]
                Rectangle:
                    pos: self.pos
                    size: self.size
            MDBoxLayout:
                id: search_results_layout
                orientation: "vertical"
                padding: [12, 8, 12, 8]
                spacing: 8
                size_hint_y: None
                height: self.minimum_height

        ScrollView:
            bar_width: 0
            MDBoxLayout:
                id: home_feed_layout
                orientation: "vertical"
                padding: [10, 12, 10, 12]
                spacing: 12
                size_hint_y: None
                height: self.minimum_height

        MDFloatingActionButton:
            icon: "plus"
            md_bg_color: [0.05, 0.45, 0.93, 1]
            pos_hint: {"center_x": .86, "center_y": .08}
            on_release: app.root.current = "add_post"

<AddPostScreen>:
    name: "add_post"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: [1, 1, 1, 1]
        MDTopAppBar:
            title: "Create Post"
            md_bg_color: [1, 1, 1, 1]
            specific_text_color: [0, 0, 0, 1]
            elevation: 0
            left_action_items: [["arrow-left", lambda x: app.go_to_home()]]
        MDBoxLayout:
            orientation: "vertical"
            padding: 20
            spacing: 15

            MDBoxLayout:
                id: preview_container
                size_hint_y: None
                height: "150dp"

            MDTextField:
                id: post_title
                hint_text: "Post Title (Optional)"
                mode: "rectangle"
            MDTextField:
                id: post_text
                hint_text: "What's on your mind?"
                mode: "rectangle"
                multiline: True
            MDRaisedButton:
                text: "Select Photo / Video"
                pos_hint: {"center_x": 0.5}
                md_bg_color: [0.4, 0.4, 0.4, 1]
                on_release: app.choose_post_photo()
            MDRaisedButton:
                text: "SHARE POST"
                pos_hint: {"center_x": 0.5}
                size_hint_x: 0.9
                md_bg_color: [0.05, 0.45, 0.93, 1]
                on_release: app.submit_new_post()

<ProfileScreen>:
    name: "profile"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: [0.93, 0.94, 0.96, 1]
        MDTopAppBar:
            title: "My Profile"
            md_bg_color: [1, 1, 1, 1]
            specific_text_color: [0, 0, 0, 1]
            elevation: 0
            left_action_items: [["arrow-left", lambda x: app.go_to_home()]]

        MDBoxLayout:
            orientation: "vertical"
            size_hint_y: None
            height: "190dp"
            md_bg_color: [1, 1, 1, 1]
            padding: 15
            spacing: 10
            FitImage:
                id: profile_pic
                source: "image"
                size_hint: None, None
                size: "84dp", "84dp"
                radius: [42, 42, 42, 42]
                pos_hint: {"center_x": 0.5}
            MDRaisedButton:
                text: "Change Profile Photo"
                size_hint_x: 0.5
                pos_hint: {"center_x": 0.5}
                on_release: app.choose_profile_photo()
            MDLabel:
                id: profile_name
                halign: "center"
                bold: True
                font_style: "H6"

        MDLabel:
            text: "   My Shared Posts"
            bold: True
            font_style: "Subtitle1"
            size_hint_y: None
            height: "45dp"
        ScrollView:
            bar_width: 0
            MDBoxLayout:
                id: profile_feed_layout
                orientation: "vertical"
                padding: [10, 0, 10, 12]
                spacing: 12
                size_hint_y: None
                height: self.minimum_height

<OtherProfileScreen>:
    name: "other_profile"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: [0.93, 0.94, 0.96, 1]
        MDTopAppBar:
            title: "User Profile"
            md_bg_color: [1, 1, 1, 1]
            specific_text_color: [0, 0, 0, 1]
            elevation: 0
            left_action_items: [["arrow-left", lambda x: app.go_to_home()]]

        MDBoxLayout:
            orientation: "vertical"
            size_hint_y: None
            height: "190dp"
            md_bg_color: [1, 1, 1, 1]
            padding: 15
            spacing: 10
            FitImage:
                id: other_profile_pic
                source: "image"
                size_hint: None, None
                size: "84dp", "84dp"
                radius: [42, 42, 42, 42]
                pos_hint: {"center_x": 0.5}
            MDLabel:
                id: other_profile_name
                halign: "center"
                bold: True
                font_style: "H6"
            MDRaisedButton:
                text: "Send Message 💬"
                pos_hint: {"center_x": 0.5}
                md_bg_color: [0.05, 0.45, 0.93, 1]
                on_release: app.open_chat(root.ids.other_profile_name.text)

        MDLabel:
            text: "   User's Shared Posts"
            bold: True
            font_style: "Subtitle1"
            size_hint_y: None
            height: "45dp"
        ScrollView:
            bar_width: 0
            MDBoxLayout:
                id: other_feed_layout
                orientation: "vertical"
                padding: [10, 0, 10, 12]
                spacing: 12
                size_hint_y: None
                height: self.minimum_height

<CommentScreen>:
    name: "comments"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: [1, 1, 1, 1]
        MDTopAppBar:
            title: "Comments"
            md_bg_color: [1, 1, 1, 1]
            specific_text_color: [0, 0, 0, 1]
            elevation: 0
            left_action_items: [["arrow-left", lambda x: app.go_to_home()]]
        ScrollView:
            MDBoxLayout:
                id: comments_layout
                orientation: "vertical"
                padding: 15
                spacing: 12
                size_hint_y: None
                height: self.minimum_height
        MDBoxLayout:
            size_hint_y: None
            height: "65dp"
            padding: [10, 5, 10, 5]
            spacing: 10
            md_bg_color: [0.96, 0.97, 0.98, 1]
            MDTextField:
                id: comment_input
                hint_text: "Write a public comment..."
                mode: "line"
            MDIconButton:
                icon: "send"
                theme_icon_color: "Custom"
                icon_color: [0.05, 0.45, 0.93, 1]
                pos_hint: {"center_y": 0.5}
                on_release: app.send_comment()

<ChatListScreen>:
    name: "chat_list"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: [1, 1, 1, 1]
        MDTopAppBar:
            title: "UniChat Chats 💬"
            md_bg_color: [1, 1, 1, 1]
            specific_text_color: [0, 0, 0, 1]
            elevation: 0
            left_action_items: [["arrow-left", lambda x: app.go_to_home()]]
        ScrollView:
            MDBoxLayout:
                id: inbox_layout
                orientation: "vertical"
                padding: 12
                spacing: 8
                size_hint_y: None
                height: self.minimum_height

<ChatScreen>:
    name: "chat"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: [0.95, 0.96, 0.98, 1]
        MDTopAppBar:
            id: chat_title
            title: "Private Chat"
            md_bg_color: [1, 1, 1, 1]
            specific_text_color: [0, 0, 0, 1]
            elevation: 0
            left_action_items: [["arrow-left", lambda x: app.go_to_chat_list()]]
        ScrollView:
            MDBoxLayout:
                id: chat_messages
                orientation: "vertical"
                padding: 15
                spacing: 10
                size_hint_y: None
                height: self.minimum_height
        MDBoxLayout:
            size_hint_y: None
            height: "65dp"
            padding: [10, 5, 10, 5]
            spacing: 10
            md_bg_color: [1, 1, 1, 1]
            MDTextField:
                id: chat_input
                hint_text: "Type a message or emoji..."
                mode: "line"
            MDIconButton:
                icon: "send"
                theme_icon_color: "Custom"
                icon_color: [0.05, 0.45, 0.93, 1]
                pos_hint: {"center_y": 0.5}
                on_release: app.send_chat_message()

<ZoomScreen>:
    name: "zoom"
    md_bg_color: [0, 0, 0, 1]
    ClickableImage:
        id: zoomed_img
        source: "image"
        size_hint: [1, 1]
        allow_stretch: True
        keep_ratio: True

<PostCard>:
    orientation: "vertical"
    size_hint_y: None
    height: "420dp"
    padding: 14
    spacing: 10
    radius: [12, 12, 12, 12]

    canvas.before:
        Color:
            rgba: [1, 1, 1, 1]
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: self.radius

    MDBoxLayout:
        size_hint_y: None
        height: "45dp"
        spacing: 10
        FitImage:
            id: user_avatar
            source: "image"
            size_hint: None, None
            size: "42dp", "42dp"
            radius: [21, 21, 21, 21]
        MDBoxLayout:
            orientation: "vertical"
            pos_hint: {"center_y": 0.5}
            MDTextButton:
                id: post_user_lbl
                text: "User Name"
                bold: True
                font_style: "Subtitle1"
                theme_text_color: "Custom"
                text_color: [0, 0, 0, 1]
                on_release: app.view_other_profile(self.text)
            MDLabel:
                text: "Shared Publicly • 🌐"
                font_style: "Caption"
                theme_text_color: "Secondary"

        Widget:

        MDIconButton:
            id: btn_delete
            icon: "delete-outline"
            theme_icon_color: "Custom"
            icon_color: [1, 0.2, 0.2, 1]
            opacity: 0
            disabled: True
            pos_hint: {"center_y": 0.5}
            on_release: app.confirm_delete_post(root.post_id)

    MDBoxLayout:
        orientation: "vertical"
        size_hint_y: None
        height: "45dp"
        spacing: 2
        MDLabel:
            id: title_lbl
            bold: True
            font_style: "Subtitle2"
        MDLabel:
            id: content_lbl
            font_style: "Body2"

    MDBoxLayout:
        id: media_container
        size_hint_y: None
        height: "195dp"

    MDBoxLayout:
        size_hint_y: None
        height: "22dp"
        padding: [4, 0, 4, 0]
        MDTextButton:
            id: likes_count_lbl
            text: "0 Reactions"
            font_style: "Caption"
            theme_text_color: "Custom"
            text_color: [0.05, 0.45, 0.93, 1]
            on_release: app.show_reactions_list(root.post_id)
        MDLabel:
            id: comments_count_lbl
            text: "0 Comments"
            halign: "right"
            font_style: "Caption"
            theme_text_color: "Secondary"

    MDSeparator:
        color: [0.9, 0.9, 0.9, 1]

    MDBoxLayout:
        size_hint_y: None
        height: "35dp"
        spacing: 2

        MDIconButton:
            id: btn_like
            icon: "thumb-up-outline"
            theme_icon_color: "Custom"
            icon_color: [0.3, 0.3, 0.3, 1]
            icon_size: "18dp"
            pos_hint: {"center_y": 0.5}
            on_release: app.submit_reaction(root, "Like 👍")
        MDIconButton:
            id: btn_love
            icon: "heart-outline"
            theme_icon_color: "Custom"
            icon_color: [0.3, 0.3, 0.3, 1]
            icon_size: "18dp"
            pos_hint: {"center_y": 0.5}
            on_release: app.submit_reaction(root, "Love ❤️")
        MDIconButton:
            id: btn_haha
            icon: "emoticon-happy-outline"
            theme_icon_color: "Custom"
            icon_color: [0.3, 0.3, 0.3, 1]
            icon_size: "18dp"
            pos_hint: {"center_y": 0.5}
            on_release: app.submit_reaction(root, "Haha 😆")

        Widget:

        MDIconButton:
            icon: "comment-outline"
            icon_size: "16dp"
            pos_hint: {"center_y": 0.5}
            on_release: app.go_to_comments(root)
        MDLabel:
            text: "Comment"
            font_style: "Caption"
            theme_text_color: "Secondary"
            size_hint_x: None
            width: "55dp"
            pos_hint: {"center_y": 0.5}
'''

class LoginScreen(Screen): pass
class RegisterScreen(Screen): pass
class HomeScreen(Screen): pass
class ProfileScreen(Screen): pass
class OtherProfileScreen(Screen): pass
class CommentScreen(Screen): pass
class ChatListScreen(Screen): pass
class ChatScreen(Screen): pass
class AddPostScreen(Screen): pass
class ZoomScreen(Screen): pass

class PostCard(MDBoxLayout):
    post_id = None
    radius = ListProperty([12, 12, 12, 12])

class CampusApp(MDApp):
    current_username = "Anonymous"
    current_profile_pic = DEFAULT_AVATAR
    active_post_id = None
    new_post_photo = "image"
    chat_partner = ""
    in_zoom_mode = False
    all_users_cache = {}

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

    def pause_all_videos(self):
        for screen in self.root.screens:
            self._pause_videos_in_widget(screen)

    def _pause_videos_in_widget(self, widget):
        if isinstance(widget, UniChatVideo):
            if widget.video.state == 'play':
                widget.video.state = 'pause'
                widget.play_btn.icon = "play"
                if widget.hide_clock:
                    widget.hide_clock.cancel()
                widget.show_controls()
        if hasattr(widget, 'children'):
            for child in widget.children:
                self._pause_videos_in_widget(child)

    def process_login(self):
        self.pause_all_videos()
        scr = self.root.get_screen('login')
        user = scr.ids.login_username.text.strip()
        password = scr.ids.login_password.text.strip()

        if user == "" or password == "":
            self.show_safe_alert("Error", "Please fill all fields!")
            return

        try:
            res = requests.get(f"{FIREBASE_URL}users/{user}.json")
            user_data = res.json()

            if user_data is None:
                self.show_safe_alert("Login Failed", "Username does not exist!")
            else:
                if user_data.get("password") == password:
                    self.current_username = user
                    self.current_profile_pic = user_data.get("pic", DEFAULT_AVATAR)
                    if not self.current_profile_pic or self.current_profile_pic == "account-circle":
                        self.current_profile_pic = DEFAULT_AVATAR
                    self.root.get_screen('profile').ids.profile_name.text = user
                    self.root.get_screen('profile').ids.profile_pic.source = self.current_profile_pic
                    self.go_to_home()
                    scr.ids.login_username.text = ""
                    scr.ids.login_password.text = ""
                else:
                    self.show_safe_alert("Login Failed", "Incorrect password!")
        except Exception as e:
            self.show_safe_alert("Network Error", "Cannot connect to server.")

    def process_registration(self):
        self.pause_all_videos()
        scr = self.root.get_screen('register')
        user = scr.ids.reg_username.text.strip()
        email = scr.ids.reg_email.text.strip()
        password = scr.ids.reg_password.text.strip()

        if user == "" or email == "" or password == "":
            self.show_safe_alert("Error", "Please fill all fields!")
            return

        if "@" not in email or "." not in email:
            self.show_safe_alert("Warning", "Please enter a valid email address!")
            return

        try:
            check_res = requests.get(f"{FIREBASE_URL}users/{user}.json")
            if check_res.json() is not None:
                self.show_safe_alert("Error", "Username is already taken!")
                return

            user_payload = {"email": email, "password": password, "pic": DEFAULT_AVATAR}
            requests.put(f"{FIREBASE_URL}users/{user}.json", json=user_payload)
            self.show_safe_alert("Success", "Registration successful! Now please log in.")
            scr.ids.reg_username.text = ""
            scr.ids.reg_email.text = ""
            scr.ids.reg_password.text = ""
            self.root.current = "login"
        except Exception as e:
            self.show_safe_alert("Network Error", "Failed to register.")

    def go_to_home(self):
        self.pause_all_videos()
        self.root.current = "home"
        pic = self.current_profile_pic
        if not pic or pic == "" or pic == "account-circle": pic = DEFAULT_AVATAR
        self.root.get_screen('home').ids.home_profile_avatar.source = pic
        self.refresh_feeds()

    def choose_profile_photo(self):
        self.pause_all_videos()
        filechooser.open_file(on_selection=self.handle_profile_photo)

    def handle_profile_photo(self, selection):
        self.pause_all_videos()
        if selection:
            self.current_profile_pic = selection[0]
            self.root.get_screen('profile').ids.profile_pic.source = selection[0]
            self.root.get_screen('home').ids.home_profile_avatar.source = selection[0]
            requests.patch(f"{FIREBASE_URL}users/{self.current_username}.json", json={"pic": selection[0]})
            self.refresh_feeds()

    def toggle_zoom_image(self, img_source):
        self.pause_all_videos()
        if not self.in_zoom_mode:
            self.root.get_screen('zoom').ids.zoomed_img.source = img_source
            self.root.current = "zoom"
            self.in_zoom_mode = True
        else:
            self.go_to_home()
            self.in_zoom_mode = False

    def filter_users(self, text):
        scr = self.root.get_screen('home')
        scroll = scr.ids.search_results_scroll
        layout = scr.ids.search_results_layout
        layout.clear_widgets()

        query = text.strip().lower()
        if query == "":
            scroll.height = "0dp"
            return

        if not self.all_users_cache:
            try:
                res = requests.get(f"{FIREBASE_URL}users.json")
                self.all_users_cache = res.json() or {}
            except:
                self.all_users_cache = {}

        users_data = self.all_users_cache
        match_found = False

        for username, data in users_data.items():
            if query in username.lower():
                match_found = True
                pic = data.get("pic", DEFAULT_AVATAR)
                if not pic or pic == "" or pic == "account-circle":
                    pic = DEFAULT_AVATAR

                row = MDBoxLayout(orientation='horizontal', size_hint_y=None, height="48dp", spacing=10)
                img = FitImage(source=pic, size_hint=(None, None), size=("36dp", "36dp"), radius=[18, 18, 18, 18],
                               pos_hint={"center_y": 0.5})

                btn = MDTextButton(text=username, bold=True, font_style="Subtitle1", pos_hint={"center_y": 0.5},
                                   theme_text_color="Custom", text_color=[0, 0, 0, 1])
                btn.bind(on_release=lambda x, u=username: self.click_search_result(u))

                row.add_widget(img)
                row.add_widget(btn)
                layout.add_widget(row)

        if match_found:
            layout_height = len(layout.children) * 52
            scroll.height = f"{min(layout_height, 160)}dp"
        else:
            scroll.height = "0dp"

    def click_search_result(self, username):
        scr = self.root.get_screen('home')
        scr.ids.search_input.text = ""
        self.view_other_profile(username)

    def refresh_feeds(self):
        home_layout = self.root.get_screen('home').ids.home_feed_layout
        prof_layout = self.root.get_screen('profile').ids.profile_feed_layout
        home_layout.clear_widgets()
        prof_layout.clear_widgets()

        try:
            users_res = requests.get(f"{FIREBASE_URL}users.json")
            users_data = users_res.json() or {}
            self.all_users_cache = users_data

            response = requests.get(f"{FIREBASE_URL}posts.json")
            posts_data = response.json() or {}

            for pid, p in posts_data.items():
                p_author = p.get('username', 'User')
                author_pic = users_data.get(p_author, {}).get('pic', DEFAULT_AVATAR)
                if not author_pic or author_pic == "" or author_pic == "account-circle":
                    author_pic = DEFAULT_AVATAR

                reacts_dict = p.get("reactions", {})
                reacts_count = len(reacts_dict) if isinstance(reacts_dict, dict) else 0
                comments_dict = p.get("comments", {})
                comments_count = len(comments_dict) if isinstance(comments_dict, dict) else 0

                card_home = self.create_post_card(pid, p_author, author_pic, p, reacts_count, comments_count,
                                                  reacts_dict, show_delete=False)
                home_layout.add_widget(card_home)

                if p_author == self.current_username:
                    card_prof = self.create_post_card(pid, p_author, author_pic, p, reacts_count, comments_count,
                                                      reacts_dict, show_delete=True)
                    prof_layout.add_widget(card_prof)
        except Exception as e:
            print(f"Error loading feeds: {e}")

    def create_post_card(self, pid, author, pic, p, r_count, c_count, reacts, show_delete=False):
        card = PostCard()
        card.post_id = pid
        card.ids.post_user_lbl.text = author
        card.ids.user_avatar.source = pic if pic and pic != "" and pic != "account-circle" else DEFAULT_AVATAR
        card.ids.title_lbl.text = p.get("title", "")
        card.ids.content_lbl.text = p.get("text", "")
        card.ids.likes_count_lbl.text = f"🔥 {r_count} Reactions"
        card.ids.comments_count_lbl.text = f"{c_count} Comments"

        media_path = p.get("img", "image")
        card.ids.media_container.clear_widgets()
        if media_path and media_path != "image":
            if media_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.3gp')):
                vid_widget = UniChatVideo(source=media_path, auto_play=False)
                card.ids.media_container.add_widget(vid_widget)
            else:
                img_widget = ClickableImage(source=media_path, allow_stretch=True, keep_ratio=True)
                card.ids.media_container.add_widget(img_widget)

        if show_delete:
            card.ids.btn_delete.opacity = 1
            card.ids.btn_delete.disabled = False

        card.ids.btn_like.icon = "thumb-up-outline"
        card.ids.btn_like.icon_color = [0.3, 0.3, 0.3, 1]
        card.ids.btn_love.icon = "heart-outline"
        card.ids.btn_love.icon_color = [0.3, 0.3, 0.3, 1]
        card.ids.btn_haha.icon = "emoticon-happy-outline"
        card.ids.btn_haha.icon_color = [0.3, 0.3, 0.3, 1]

        if self.current_username in reacts:
            user_react = reacts[self.current_username]
            if "Like" in user_react:
                card.ids.btn_like.icon = "thumb-up"
                card.ids.btn_like.icon_color = [0.05, 0.45, 0.93, 1]
            elif "Love" in user_react:
                card.ids.btn_love.icon = "heart"
                card.ids.btn_love.icon_color = [1, 0.2, 0.2, 1]
            elif "Haha" in user_react:
                card.ids.btn_haha.icon = "emoticon-happy"
                card.ids.btn_haha.icon_color = [1, 0.7, 0, 1]
        return card

    def show_reactions_list(self, post_id):
        try:
            users_res = requests.get(f"{FIREBASE_URL}users.json")
            users_data = users_res.json() or {}

            res = requests.get(f"{FIREBASE_URL}posts/{post_id}/reactions.json")
            reacts_data = res.json() or {}

            main_layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)

            from kivy.uix.scrollview import ScrollView
            scroll = ScrollView(bar_width=0)
            list_layout = MDBoxLayout(orientation='vertical', spacing=12, size_hint_y=None)
            list_layout.bind(minimum_height=list_layout.setter('height'))

            if reacts_data:
                for user, react_type in reacts_data.items():
                    pic = users_data.get(user, {}).get('pic', DEFAULT_AVATAR)
                    if not pic or pic == "" or pic == "account-circle":
                        pic = DEFAULT_AVATAR

                    row = MDBoxLayout(orientation='horizontal', size_hint_y=None, height="50dp", spacing=12)
                    img = FitImage(source=pic, size_hint=(None, None), size=("40dp", "40dp"), radius=[20, 20, 20, 20])
                    lbl_name = MDLabel(text=f"[b]{user}[/b]", markup=True, size_hint_x=0.6, pos_hint={"center_y": 0.5})
                    lbl_react = MDLabel(text=react_type, halign="right", size_hint_x=0.4, pos_hint={"center_y": 0.5})

                    row.add_widget(img)
                    row.add_widget(lbl_name)
                    row.add_widget(lbl_react)
                    list_layout.add_widget(row)
            else:
                list_layout.add_widget(
                    Label(text="No reactions yet.", color=[1, 1, 1, 1], size_hint_y=None, height="40dp"))

            scroll.add_widget(list_layout)
            main_layout.add_widget(scroll)

            close_btn = Button(text="Close", size_hint_y=None, height="40dp", background_color=[0.05, 0.45, 0.93, 1])
            main_layout.add_widget(close_btn)

            popup = Popup(title="People who reacted", content=main_layout, size_hint=(0.85, 0.5))
            close_btn.bind(on_release=popup.dismiss)
            popup.open()
        except Exception as e:
            print(f"Error loading reactions popup: {e}")

    def confirm_delete_post(self, post_id):
        main_layout = MDBoxLayout(orientation='vertical', padding=15, spacing=15)

        msg_lbl = Label(text="Are you sure you want to delete this post?", color=[1, 1, 1, 1], halign="center")
        msg_lbl.bind(size=lambda s, w: setattr(s, 'text_size', (w[0] * 0.9, None)))
        main_layout.add_widget(msg_lbl)

        btn_layout = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height="45dp")
        yes_btn = Button(text="Yes, Delete", background_color=[1, 0.2, 0.2, 1])
        no_btn = Button(text="No, Cancel", background_color=[0.3, 0.3, 0.3, 1])

        btn_layout.add_widget(yes_btn)
        btn_layout.add_widget(no_btn)
        main_layout.add_widget(btn_layout)

        popup = Popup(title="Delete Confirmation", content=main_layout, size_hint=(0.85, 0.28), auto_dismiss=False)
        yes_btn.bind(on_release=lambda x: self.execute_post_deletion(post_id, popup))
        no_btn.bind(on_release=popup.dismiss)
        popup.open()

    def execute_post_deletion(self, post_id, popup):
        try:
            requests.delete(f"{FIREBASE_URL}posts/{post_id}.json")
            popup.dismiss()
            self.refresh_feeds()
        except Exception as e:
            print(f"Delete failed: {e}")

    def show_safe_alert(self, title, message):
        box = MDBoxLayout(orientation='vertical', padding=15, spacing=15)

        lbl = Label(text=message, color=[1, 1, 1, 1], halign="center", valign="middle")
        lbl.bind(size=lambda s, w: setattr(s, 'text_size', (w[0] * 0.9, None)))
        box.add_widget(lbl)

        ok_btn = Button(text="OK", size_hint_y=None, height="40dp", background_color=[0.05, 0.45, 0.93, 1])
        box.add_widget(ok_btn)

        popup = Popup(title=title, content=box, size_hint=(0.85, 0.28))
        ok_btn.bind(on_release=popup.dismiss)
        popup.open()

    def view_other_profile(self, username):
        self.pause_all_videos()
        self.root.current = "other_profile"
        scr = self.root.get_screen("other_profile")
        scr.ids.other_profile_name.text = username
        layout = scr.ids.other_feed_layout
        layout.clear_widgets()

        try:
            users_res = requests.get(f"{FIREBASE_URL}users.json")
            users_data = users_res.json() or {}

            pic = users_data.get(username, {}).get('pic', DEFAULT_AVATAR)
            if not pic or pic == "" or pic == "account-circle": pic = DEFAULT_AVATAR
            scr.ids.other_profile_pic.source = pic

            response = requests.get(f"{FIREBASE_URL}posts.json")
            posts_data = response.json() or {}

            for pid, p in posts_data.items():
                if p.get('username') == username:
                    reacts_dict = p.get("reactions", {})
                    reacts_count = len(reacts_dict) if isinstance(reacts_dict, dict) else 0
                    card = self.create_post_card(pid, username, pic, p, reacts_count, 0, reacts_dict, show_delete=False)
                    layout.add_widget(card)
        except Exception as e:
            print(f"Error viewing profile: {e}")

    def go_to_chat_list(self):
        self.pause_all_videos()
        self.root.current = "chat_list"
        layout = self.root.get_screen("chat_list").ids.inbox_layout
        layout.clear_widgets()

        try:
            users_res = requests.get(f"{FIREBASE_URL}users.json")
            users_data = users_res.json() or {}

            chats_res = requests.get(f"{FIREBASE_URL}chats.json")
            chats_data = chats_res.json() or {}

            active_partners = set()
            for chat_id in chats_data.keys():
                if self.current_username in chat_id:
                    partner = chat_id.replace(self.current_username, "")
                    if partner:
                        active_partners.add(partner)

            for partner in active_partners:
                partner_pic = users_data.get(partner, {}).get('pic', DEFAULT_AVATAR)
                if not partner_pic or partner_pic == "" or partner_pic == "account-circle": partner_pic = DEFAULT_AVATAR

                row = MDBoxLayout(orientation='horizontal', size_hint_y=None, height="65dp", spacing=15, padding=10)
                img = FitImage(source=partner_pic, size_hint=(None, None), size=("46dp", "46dp"),
                               radius=[23, 23, 23, 23])

                btn = MDTextButton(text=partner, bold=True, font_style="H6", pos_hint={"center_y": 0.5})
                btn.bind(on_release=lambda x, p=partner: self.open_chat(p))

                row.add_widget(img)
                row.add_widget(btn)
                layout.add_widget(row)
        except Exception as e:
            print(f"Inbox load error: {e}")

    def open_chat(self, partner_name):
        self.pause_all_videos()
        self.chat_partner = partner_name
        self.root.current = "chat"
        self.root.get_screen("chat").ids.chat_title.title = f"Chat with {partner_name}"
        self.load_chat()

    def load_chat(self):
        layout = self.root.get_screen("chat").ids.chat_messages
        layout.clear_widgets()
        chat_id = "".join(sorted([self.current_username, self.chat_partner]))
        try:
            response = requests.get(f"{FIREBASE_URL}chats/{chat_id}.json")
            messages = response.json() or {}
            for mid, m in messages.items():
                align = "right" if m['user'] == self.current_username else "left"
                color = [0.05, 0.45, 0.93, 1] if m['user'] == self.current_username else [0.2, 0.2, 0.2, 1]
                lbl = MDLabel(text=f"[b]{m['user']}:[/b] {m['text']}", markup=True, halign=align,
                              theme_text_color="Custom", text_color=color, size_hint_y=None, height="30dp")
                layout.add_widget(lbl)
        except Exception as e:
            print(f"Chat load error: {e}")

    def send_chat_message(self):
        scr = self.root.get_screen("chat")
        text = scr.ids.chat_input.text
        if text.strip() != "":
            chat_id = "".join(sorted([self.current_username, self.chat_partner]))
            data = {"user": self.current_username, "text": text}
            requests.post(f"{FIREBASE_URL}chats/{chat_id}.json", json=data)
            scr.ids.chat_input.text = ""
            self.load_chat()

    def choose_post_photo(self):
        filechooser.open_file(on_selection=self.handle_post_photo)

    def handle_post_photo(self, selection):
        if selection:
            self.new_post_photo = selection[0]
            scr = self.root.get_screen('add_post')
            scr.ids.preview_container.clear_widgets()

            if self.new_post_photo.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.3gp')):
                vid = UniChatVideo(source=self.new_post_photo, auto_play=True)
                scr.ids.preview_container.add_widget(vid)
            else:
                img = Image(source=self.new_post_photo, allow_stretch=True, keep_ratio=True)
                scr.ids.preview_container.add_widget(img)

    def submit_new_post(self):
        scr = self.root.get_screen('add_post')
        new_post = {
            "username": self.current_username,
            "title": scr.ids.post_title.text,
            "text": scr.ids.post_text.text,
            "img": self.new_post_photo,
            "reactions": {},
            "comments": {}
        }
        requests.post(f"{FIREBASE_URL}posts.json", data=json.dumps(new_post))
        scr.ids.post_title.text = ""
        scr.ids.post_text.text = ""
        scr.ids.preview_container.clear_widgets()
        self.new_post_photo = "image"
        self.go_to_home()

    def submit_reaction(self, card, react_type):
        res = requests.get(f"{FIREBASE_URL}posts/{card.post_id}/reactions.json")
        current_reacts = res.json() or {}
        if self.current_username in current_reacts and current_reacts[self.current_username] == react_type:
            requests.delete(f"{FIREBASE_URL}posts/{card.post_id}/reactions/{self.current_username}.json")
        else:
            requests.put(f"{FIREBASE_URL}posts/{card.post_id}/reactions/{self.current_username}.json", json=react_type)
        self.refresh_feeds()

    def go_to_comments(self, card):
        self.pause_all_videos()
        self.active_post_id = card.post_id
        self.root.current = "comments"
        self.load_comments()

    def load_comments(self):
        layout = self.root.get_screen('comments').ids.comments_layout
        layout.clear_widgets()
        response = requests.get(f"{FIREBASE_URL}posts/{self.active_post_id}/comments.json")
        comments_data = response.json() or {}
        for cid, c in comments_data.items():
            c_box = MDBoxLayout(orientation='horizontal', size_hint_y=None, height="45dp", spacing=10)
            pic = c.get('pic', DEFAULT_AVATAR)
            if not pic or pic == "" or pic == "account-circle": pic = DEFAULT_AVATAR
            img = FitImage(source=pic, size_hint=(None, None), size=("35dp", "35dp"), radius=[17, 17, 17, 17])
            lbl = MDLabel(text=f"[b]{c.get('user', 'User')}:[/b] {c.get('text', '')}", markup=True)
            c_box.add_widget(img)
            c_box.add_widget(lbl)
            layout.add_widget(c_box)

    def send_comment(self):
        scr = self.root.get_screen('comments')
        text = scr.ids.comment_input.text
        if text.strip() != "":
            comment_payload = {"user": self.current_username, "text": text, "pic": self.current_profile_pic}
            requests.post(f"{FIREBASE_URL}posts/{self.active_post_id}/comments.json", json=comment_payload)
            scr.ids.comment_input.text = ""
            self.load_comments()

    def go_to_profile(self):
        self.pause_all_videos()
        self.root.current = "profile"
        self.refresh_feeds()

if __name__ == "__main__":
    CampusApp().run()
