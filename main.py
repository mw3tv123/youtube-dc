# .-------------------.
# |      imports      |
# '-------------------'
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.image import AsyncImage

from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import TwoLineAvatarListItem, ILeftBody
from kivymd.theming import ThemeManager

from lib.coreprocess import CoreProcess

# This construct UI components for App
main_widget_kv = '''
#:import Toolbar kivymd.toolbar.Toolbar
#:import MDTextField kivymd.textfields.MDTextField
#:import MDSpinner kivymd.spinner.MDSpinner
#:import get_color_from_hex kivy.utils.get_color_from_hex

# Toolbar on the top of every screem
<ScreenToolbar@Toolbar>:
    pos_hint: {'center_x': 0.5, 'top': 1}
    md_bg_color: get_color_from_hex(colors['Teal']['500'])
    background_palette: 'DeepPurple'
    background_hue: 'A400'

# Main UI
ScreenManager:
    # Main_Screen
    Screen:
        id: main_screen
        name: 'Main_Screen'
        manager: 'screen_manager'
        on_enter: app.clear_cache()
        ScreenToolbar:
            right_action_items: [['settings', lambda x: app.change_screen('Setting_Screen')]]
        MDTextField:
            id: data_text
            pos_hint: {'center_x': 0.5, 'center_y': 0.6}
            size_hint: 0.8, None
            hint_text: "Enter keywords or URL"
            on_text_validate: app.get_user_data()
        MDRaisedButton:
            text: "PROCESS"
            elevation_normal: 2
            opposite_colors: True
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            on_press: app.get_user_data()

    # Search_Screen
    Screen:
        id: search_screen
        name: 'Search_Screen'
        manager: 'screen_manager'
        on_enter: app.search_keywords()
        ScreenToolbar
            left_action_items: [['home', lambda x: app.change_screen('Main_Screen')]]
            right_action_items: [['settings', lambda x: app.change_screen('Setting_Screen')]]
        ScrollView:
            pos_hint: {'x': 0, 'top': 0.85}
            do_scroll_x: False
            MDList:
                id: result_list
                MDSpinner:
                    size_hint: None, None
                    size: dp(46), dp(46)
                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                    active: True

    # Download_Screen
    Screen:
        id: download_screen
        name: 'Download_Screen'
        manager: 'screen_manager'
        on_enter: app.download_video()
        ScreenToolbar
            left_action_items: [['home', lambda x: app.change_screen('Main_Screen')]]
            right_action_items: [['settings', lambda x: app.change_screen('Setting_Screen')]]

    # Setting_Screen
    Screen:
        id: setting_screen
        name: 'Setting_Screen'
        manager: 'screen_manager'
        ScreenToolbar
            left_action_items: [['home', lambda x: app.change_screen('Main_Screen')]]
'''


# .-------------------.
# |      classes      |
# '-------------------'
class YouTubeDownloader(App):
    """One Class maintains all stuffs"""
    theme_cls = ThemeManager()
    core_process = CoreProcess()
    user_input = ''
    previousScreen = ''

    def build(self):
        """Build UI"""
        self.theme_cls.theme_style = 'Dark'
        self.main_widget = Builder.load_string(main_widget_kv)
        Window.size = (360, 640)
        return self.main_widget

    def get_user_data(self):
        """Base on user input to determine which screen next"""
        if self.main_widget.ids.data_text.text:
            self.user_input = self.main_widget.ids.data_text.text
            if self.user_input.startswith(('https', 'http')):
                next_screen = 'Download_Screen'
            else:
                next_screen = 'Search_Screen'
            self.main_widget.current = next_screen
        
        # If user does not give us anything, a pop up will remind they
        else:
            content = MDLabel(font_style='Body1',
                              theme_text_color='Secondary',
                              text="You need to enter something for me!",
                              size_hint_y=None,
                              valign='top')
            content.bind(texture_size=content.setter('size'))
        
            dialog = MDDialog(title="There's nothing for me to do",
                              content=content,
                              size_hint=(.9, None),
                              height=dp(200),
                              auto_dismiss=False)
            dialog.add_action_button("Dismiss", action=lambda *x: dialog.dismiss())
            dialog.open()

    def clear_cache(self):
        """Clears recently cache data in this screen"""
        self.main_widget.ids.data_text.text = ''

    def change_screen(self, next_screen):
        """Change to another screen"""
        self.main_widget.current = next_screen

    def search_keywords(self):
        """Processes user data"""
        result = self.core_process.search_by_keywords(self.user_input)
        self.show_result(result)

    def show_result(self, data):
        """Show search result"""
        self.main_widget.ids.result_list.clear_widgets()
        for i in range(len(data['links'])):
            video = TwoLineAvatarListItem(text=data['title'][i],
                                          secondary_text=data['links'][i])
            video.add_widget(VideoThumbnail(source=data['images'][i]))
            self.main_widget.ids.result_list.add_widget(video)
            # video.bind(on_press=(self.change_screen('Download_Screen'), self.download_video(data['links'][i])))

    def download_video(self, url):
        self.core_process.download_video(url)


class VideoThumbnail(ILeftBody, AsyncImage):
    pass


if __name__ == '__main__':
    YouTubeDownloader().run()
