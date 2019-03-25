# .-------------------.
# |      imports      |
# '-------------------'
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import AsyncImage

from kivymd.button import MDIconButton
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.theming import ThemeManager

from lib.coreprocess import CoreProcess


# .-------------------.
# |      classes      |
# '-------------------'
# Base class of navigation button on the top
class MyBaseButton(MDIconButton):
    """Dummy Base Button class for navigation button"""
    pass


class SettingButton(MyBaseButton):
    """Dummy Setting Button class inherited from Base Button"""
    icon = StringProperty('settings')


class HomeButton(MyBaseButton):
    """Dummy Home Button class inherited from Base Button"""
    icon = StringProperty('home')


class BackButton(MyBaseButton):
    """Dummy Back Button class inherited from Base Button"""
    icon = StringProperty('backspace')
# --->>>    End of dummy button class   <<<--- #


class VideoThumbnail(ILeftBodyTouch, AsyncImage):
    """Video Thumbnail on the left"""
    pass


# --->>>    Main    <<<--- #
class MainScreen(Screen):
    """
    Main Screen also Landing Screen, where user first launch the App.
    Receive user 'search keywords' or 'download URL' then process to the Detail Screen.
    """
    user_input = ''

    def get_user_data(self, root):
        """Base on user to determine which screen next"""
        if self.ids.data_text.text:
            self.user_input = self.ids.data_text.text
            
            if self.user_input.startswith(('https', 'http')):
                next_screen = 'Download_Screen'
            else:
                next_screen = 'Search_Screen'
            self.change_screen(root, next_screen)
        else:
            content = MDLabel(font_style='Body1',
                              theme_text_color='Secondary',
                              text="You need to enter something for me!",
                              size_hint_y=None,
                              valign='top')
            content.bind(texture_size=content.setter('size'))
            
            self.dialog = MDDialog(title="There's nothing for me to do",
                                   content=content,
                                   size_hint=(.9, None),
                                   height=dp(200),
                                   auto_dismiss=False)
            self.dialog.add_action_button("Dismiss",
                                          action=lambda *x: self.dialog.dismiss())
            self.dialog.open()

    def change_screen(self, root, next_screen):
        """Changes to specific screen base on user data"""
        root.previousScreen = self.name
        root.transition.direction = 'left'
        root.current = next_screen

    def clear_cache(self):
        """Clears recently cache data in this screen"""
        self.ids.data_text.text = ''


class SearchScreen(Screen):
    """
    Search Screen receive user data from Main Screen then process base on data input.
    Result will show here for user.
    """
    user_data = ''

    def process_request(self):
        """Processes user data"""
        self.user_data = core_process.search_by_keywords(self.user_data)
        self.show_result()

    def show_result(self):
        """Show search result"""
        self.ids.result_list.clear_widgets()
        for i in range(len(self.user_data['links'])):
            video = TwoLineAvatarIconListItem(
                text=self.user_data['title'][i],
                secondary_text=self.user_data['links'][i],
            )
            video.add_widget(VideoThumbnail(source=self.user_data['images'][i]))
            self.ids.result_list.add_widget(video)


class DownloadScreen(Screen):
    """Download Screen is where user wait to download the video"""
    def download_soundtrack(self, url):
        """Downloads sound back to device"""
        core_process.download_video(url)


class SettingScreen(Screen):
    """Dummy Setting Screen for user configure App setting"""
    pass


class ScreenControl(ScreenManager):
    """Dummy class for manager screens"""
    mainScreen = ObjectProperty(None)
    searchScreen = ObjectProperty(None)
    downloadScreen = ObjectProperty(None)
    settingScreen = ObjectProperty(None)
    previousScreen = StringProperty('')

    def transfer_data(self):
        """Transfers data from Main Screen to Another Screen when it take focus.
        A work around method to transfer data from screen to screen at the moment (Update in the future)."""
        if self.current == 'Search_Screen':
            if self.previousScreen == 'Main_Screen':
                self.searchScreen.user_data = self.mainScreen.user_input
                self.searchScreen.process_request()
            
        if self.current == 'Download_Screen':
            self.downloadScreen.download_soundtrack(self.mainScreen.user_input)


# .-------------------.
# |      global       |
# '-------------------'
core_process = CoreProcess()
buildKV = Builder.load_file("uimanager.kv")


class MyApp(App):
    """Dummy class for running app"""
    theme_cls = ThemeManager()

    def build(self):
        Window.size = (360, 640)
        return buildKV


if __name__ == '__main__':
    MyApp().run()
