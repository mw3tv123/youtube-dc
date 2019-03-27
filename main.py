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

# .-------------------.
# |       App UI      |
# '-------------------'
main_widget_kv = '''
#:import Toolbar kivymd.toolbar.Toolbar
#:import MDTextField kivymd.textfields.MDTextField
#:import MDDropdownMenu kivymd.menu.MDDropdownMenu
#:import MDMenuItem kivymd.menu.MDMenuItem
#:import MDCheckbox kivymd.selectioncontrols.MDCheckbox
#:import MDSpinner kivymd.spinner.MDSpinner
#:import get_color_from_hex kivy.utils.get_color_from_hex

# Toolbar on the top of every screen
<Toolbar>:
    pos_hint:           {'center_x': 0.5, 'top': 1}
    md_bg_color:        get_color_from_hex(colors['Teal']['500'])
    background_palette: 'DeepPurple'
    background_hue:     'A400'

# Add event handler when an item is press and release
<MDMenuItem>:
    on_release: app.change_options(self.text)

# Main UI
ScreenManager:
    # Main_Screen
    Screen:
        id:       main_screen
        name:     'Main_Screen'
        manager:  'screen_manager'
        on_enter: app.clear_cache()
        Toolbar:
            right_action_items: [['settings', lambda x: app.change_screen('Setting_Screen')]]
        # Receive user data
        MDTextField:
            id:               data_text
            pos_hint:         {'center_x': 0.5, 'center_y': 0.6}
            size_hint:        0.8, None
            hint_text:        "Enter keywords or URL"
            on_text_validate: app.get_user_data()
        MDRaisedButton:
            text:             "PROCESS"
            elevation_normal: 2
            opposite_colors:  True
            pos_hint:         {'center_x': 0.5, 'center_y': 0.5}
            on_press:         app.get_user_data()

    # Search_Screen
    Screen:
        id:       search_screen
        name:     'Search_Screen'
        manager:  'screen_manager'
        on_enter: app.search_keywords()
        Toolbar:
            left_action_items:  [['home', lambda x: app.change_screen('Main_Screen')]]
            right_action_items: [['settings', lambda x: app.change_screen('Setting_Screen')]]
        # Display all videos we search to the user
        ScrollView:
            pos_hint:    {'x': 0, 'top': 0.85}
            do_scroll_x: False
            MDList:
                id: result_list
                # This spinner is used for display "search process" and is removed when we get the result
                # But currently not work as expected, will fix in the future
                MDSpinner:
                    size_hint: None, None
                    size:      dp(46), dp(46)
                    pos_hint:  {'center_x': 0.5, 'center_y': 0.5}
                    active:    True

    # Download_Screen
    Screen:
        id:       download_screen
        name:     'Download_Screen'
        manager:  'screen_manager'
        on_enter: app.download_video()
        Toolbar:
            left_action_items:  [['home', lambda x: app.change_screen('Main_Screen')]]
            right_action_items: [['settings', lambda x: app.change_screen('Setting_Screen')]]

    # Setting_Screen
    Screen:
        id:      setting_screen
        name:    'Setting_Screen'
        manager: 'screen_manager'
        Toolbar:
            left_action_items: [['home', lambda x: app.change_screen('Main_Screen')]]
        # Display setting for user configure
        GridLayout:
            id:      options_layout
            cols:    2
            padding: '10dp'
            # File extensions option
            MDLabel:
                font_style:       'Subhead'
                theme_text_color: 'Primary'
                text_color:       (0,1,0,.4)
                text:             "File extension"
                halign:           'center'
            MDRaisedButton:
                id:              ext_opts
                text:            app.core_process.options['postprocessors'][0]['preferredcodec']
                size_hint:       None, None
                size:            3 * dp(18), dp(28)
                pos_hint:        {'center_x': 0.5, 'center_y': 0.5}
                opposite_colors: True
                on_release:      MDDropdownMenu(items=app.audio_extensions).open(self)
            # Quality option
            MDLabel:
                font_style:       'Subhead'
                theme_text_color: 'Primary'
                text_color:       (0, 1, 0, .4)
                text:             "Quality"
                halign:           'center'
            MDRaisedButton:
                id:              quality_opts
                text:            'Best' if app.core_process.options['format'] == 'bestaudio' else 'Worst'
                size_hint:       None, None
                size:            3 * dp(18), dp(28)
                pos_hint:        {'center_x': 0.5, 'center_y': 0.5}
                opposite_colors: True
                on_release:      MDDropdownMenu(items=app.audio_qualities, width_mult=4).open(self)
            MDLabel:
                font_style:       'Subhead'
                theme_text_color: 'Primary'
                text_color:       (0, 1, 0, .4)
                text:             "Restricted filename"
                halign:           'center'
            # Restrict file name option
            MDCheckbox:
                id:        restrict_filename_cb
                size_hint: None, None
                size:      dp(48), dp(48)
                pos_hint:  {'center_x': 0.5, 'center_y': 0.4}
                active:    app.core_process.options['restrictfilenames']
                on_state: app.core_process.options['restrictfilenames'] = self.active
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
    audio_extensions = [{'viewclass': 'MDMenuItem',
                         'text': 'best'},
                        {'viewclass': 'MDMenuItem',
                         'text': 'aac'},
                        {'viewclass': 'MDMenuItem',
                         'text': 'flac'},
                        {'viewclass': 'MDMenuItem',
                         'text': 'mp3'},
                        {'viewclass': 'MDMenuItem',
                         'text': 'm4a'},
                        {'viewclass': 'MDMenuItem',
                         'text': 'opus'},
                        {'viewclass': 'MDMenuItem',
                         'text': 'vorbis'},
                        {'viewclass': 'MDMenuItem',
                         'text': 'wav'}]
    audio_qualities = [{'viewclass': 'MDMenuItem',
                        'text': 'Best'},
                       {'viewclass': 'MDMenuItem',
                        'text': 'Worst'}]

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
        """Just download the video base on the option"""
        self.core_process.download_video(url)

    def change_options(self, text):
        """"""
        if text == 'Best Audio':
            self.main_widget.ids.quality_opts.text = text
            self.core_process.options['format'] = 'bestaudio'
        if text == 'Worst Audio':
            self.main_widget.ids.quality_opts.text = text
            self.core_process.options['format']  = 'worstaudio'
        else:
            self.main_widget.ids.ext_opts.text = text
            self.core_process.options['postprocessors'][0]['preferredcodec'] = text
        print(self.core_process.options)


class VideoThumbnail(ILeftBody, AsyncImage):
    pass


if __name__ == '__main__':
    YouTubeDownloader().run()
