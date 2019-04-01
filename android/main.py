# .-------------------.
# |      imports      |
# '-------------------'
from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.network.urlrequest import UrlRequest
from kivy.properties import NumericProperty
from kivy.uix.image import AsyncImage

from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import TwoLineAvatarListItem, ILeftBody
from kivymd.theming import ThemeManager

from bs4 import BeautifulSoup
import json
from plyer import storagepath
import os
from threading import Thread
import time
from urllib.parse import quote
import youtube_dl
# .-------------------.
# |       App UI      |
# '-------------------'
main_widget_kv = '''
#:import Toolbar kivymd.toolbar.Toolbar
#:import MDCheckbox kivymd.selectioncontrols.MDCheckbox
#:import MDDropdownMenu kivymd.menu.MDDropdownMenu
#:import MDMenuItem kivymd.menu.MDMenuItem
#:import MDProgressBar kivymd.progressbar.MDProgressBar
#:import MDSpinner kivymd.spinner.MDSpinner
#:import MDTextField kivymd.textfields.MDTextField
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
            right_action_items: [['settings', lambda x: app.change_screen(next_screen='Setting_Screen')]]
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
            left_action_items:  [['home', lambda x: app.change_screen(next_screen='Main_Screen')]]
            right_action_items: [['settings', lambda x: app.change_screen(next_screen='Setting_Screen')]]
        # Display all videos we search to the user
        ScrollView:
            pos_hint:    {'x': 0, 'top': 0.85}
            do_scroll_x: False
            MDList:
                id: result_list
                size: self.parent.size
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
        Toolbar:
            left_action_items:  [['home', lambda x: app.change_screen(next_screen='Main_Screen')]]
            right_action_items: [['settings', lambda x: app.change_screen(next_screen='Setting_Screen')]]
        MDLabel:
            id:               video_title_label
            font_style:       'Subhead'
            theme_text_color: 'Primary'
            text_color:       (0, 1, 0, .4)
            halign:           'center'
        MDProgressBar:
            size_hint_x: 0.8
            pos_hint:    {'x': 0.1} 
            value:       app.progress_percent

    # Setting_Screen
    Screen:
        id:      setting_screen
        name:    'Setting_Screen'
        manager: 'screen_manager'
        Toolbar:
            left_action_items: [['home', lambda x: app.change_screen(next_screen='Main_Screen')]]
        # Display setting for user configure
        BoxLayout:
            orientation: 'vertical'
            spacing:     dp(15)
            pos_hint:    {'center_x': 1, 'center_y': 0.5}
            # File extensions option
            BoxLayout:
                size:      dp(48)*3, dp(48)
                size_hint: (None, None)
                MDLabel:
                    font_style:       'Subhead'
                    theme_text_color: 'Primary'
                    text_color:       (0,1,0,.4)
                    text:             "File extension"
                    halign:           'center'
                    size_hint:        None, None
                    size:             dp(130), dp(48)
                MDRaisedButton:
                    id:              ext_opts
                    text:            app.options['postprocessors'][0]['preferredcodec']
                    size_hint:       None, None
                    size:            3 * dp(18), dp(28)
                    opposite_colors: True
                    on_release:      MDDropdownMenu(items=app.audio_extensions).open(self)
            # Quality option
            BoxLayout:
                size:      dp(48)*3, dp(48)
                size_hint: (None, None)
                MDLabel:
                    font_style:       'Subhead'
                    theme_text_color: 'Primary'
                    text_color:       (0, 1, 0, .4)
                    text:             "Quality"
                    halign:           'center'
                    size_hint:        None, None
                    size:             dp(130), dp(48)
                MDRaisedButton:
                    id:              quality_opts
                    text:            'Best' if app.options['format'] == 'bestaudio' else 'Worst'
                    size_hint:       None, None
                    size:            3 * dp(18), dp(28)
                    opposite_colors: True
                    on_release:      MDDropdownMenu(items=app.audio_qualities, width_mult=4).open(self)
            # Restrict file name option
            BoxLayout:
                size:      dp(48)*3, dp(48)
                size_hint: (None, None)
                MDLabel:
                    font_style:       'Subhead'
                    theme_text_color: 'Primary'
                    text_color:       (0, 1, 0, .4)
                    text:             "Restricted filename"
                    halign:           'center'
                    size_hint:        None, None
                    size:             dp(130), dp(48)
                MDCheckbox:
                    id:        restrict_filename_cb
                    size_hint: None, None
                    size:      dp(48), dp(48)
                    pos_hint:  {'center_x': 0.5, 'center_y': 0.4}
                    active:    app.options['restrictfilenames']
                    on_state:  app.options['restrictfilenames'] = self.active
'''


# .-------------------.
# |      classes      |
# '-------------------'
class LogHandler(object):
    """LogHandler handle messages for each case"""
    @staticmethod
    def debug(msg):
        pass

    @staticmethod
    def warning(msg):
        notify_observers(msg, mode="warning")

    @staticmethod
    def error(msg):
        notify_observers(msg, mode="error")


class YouTubeDownloader(App):
    """App class maintains all stuffs"""
    theme_cls = ThemeManager()
    user_input = ''
    previousScreen = ''
    progress_percent = NumericProperty(0)
    # Audio output extensions
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
    # Audio output quality
    audio_qualities = [{'viewclass': 'MDMenuItem',
                        'text': 'Best'},
                       {'viewclass': 'MDMenuItem',
                        'text': 'Worst'}]
    # Path to file contain setting configuration
    config_path = storagepath.get_application_dir() + '/config.txt'

    def build(self):
        """Start App"""
        self.theme_cls.theme_style = 'Dark'
        self.load_settings()
        self.main_widget = Builder.load_string(main_widget_kv)
        return self.main_widget

    def load_settings(self):
        """Initiate setting by create a new options structure and load from local file if configuration file existed."""
        default_storage_directory = storagepath.get_application_dir() + "/my_audio/"
        # Check if Download folder exist or not. If not then we create it
        if not os.path.isdir(default_storage_directory):
            os.mkdir(default_storage_directory)
        file_sample = "%(title)s.%(ext)s"
        self.options = {
            'format': 'bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': default_storage_directory + file_sample,
            'restrictfilenames': False,
            'debug_printtraffic': False,
            'logger': LogHandler(),
            'progress_hooks': [self.process_handler],
            'simulate': False,
            'forcedescription': False,
            'forcetitle': False,
        }
        # If old setting detected, load it
        if os.path.isfile(self.config_path):
            with open(self.config_path) as file:
                data = json.load(file)
                if 'format' in data:
                    self.options['format'] = data['format']
                if 'postprocessors' in data:
                    self.options['postprocessors'].clear()
                    self.options['postprocessors'] = data['postprocessors']
                if 'restrictfilenames' in data:
                    self.options['restrictfilenames'] = data['restrictfilenames']
        else:  # If not, create a new one
            self.save_setting()

    def change_options(self, text):
        """Call when user change an option in Setting Screen"""
        if text == 'Best':
            self.main_widget.ids.quality_opts.text = text
            self.options['format'] = 'bestaudio'
        if text == 'Worst':
            self.main_widget.ids.quality_opts.text = text
            self.options['format'] = 'worstaudio'
        else:
            self.main_widget.ids.ext_opts.text = text
            self.options['postprocessors'][0]['preferredcodec'] = text

    def save_setting(self):
        """Save setting configuration to file"""
        data = {}
        for k, v in self.options.items():
            if isinstance(v, LogHandler):
                continue
            if type(v) == list and callable(v[0]):
                continue
            data[k] = v
        with open(self.config_path, "w") as file:
            json.dump(data, file)

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

    def change_screen(self, **kwargs):
        """Change to another screen"""
        self.main_widget.current = kwargs['next_screen']
        if 'title' in kwargs:
            self.main_widget.ids.video_title_label.text = kwargs['title']
            self.downloading_process(kwargs['url'])

    def search_keywords(self):
        """Processes user data"""
        query = quote(self.user_input)
        search_url = "https://www.youtube.com/results?search_query=" + query
        UrlRequest(url=search_url, on_success=self.scrap_result)

    def scrap_result(self, request, response):
        """Scrap all info we need in the response text"""
        del request
        soup = BeautifulSoup(response, 'html.parser')
        result = {
            'links': [],
            'images': [],
            'title': [],
        }
        # Split only video tag
        for video in soup.find_all(attrs={'class': 'yt-uix-tile-link'}):
            if not video['href'].split('=')[1].endswith('list'):
                result['links'].append("https://www.youtube.com" + video['href'])
                result['images'].append("http://img.youtube.com/vi/" + video['href'].split('=')[1] + "/hqdefault.jpg")
                result['title'].append(video['title'])
        self.show_result(result)

    def _get_video_description(self):
        pass

    def show_result(self, data):
        """Show search result"""
        self.main_widget.ids.result_list.clear_widgets()
        for i in range(len(data['links'])):
            video = TwoLineAvatarListItem(text=data['title'][i],
                                          secondary_text=data['links'][i])
            # noinspection PyArgumentList
            video.add_widget(VideoThumbnail(source=data['images'][i]))
            self.main_widget.ids.result_list.add_widget(video)
            video.bind(on_press=lambda event: self.change_screen(next_screen='Download_Screen',
                                                                 title=data['title'][i],
                                                                 url=data['links'][i],
                                                                 ))

    def downloading_process(self, link):
        """Just download the video base on the option"""
        def download_video(url):
            with youtube_dl.YoutubeDL(self.options) as ydl:
                if type(url) == str:
                    ydl.download([url])
                else:
                    for element in url:
                        ydl.download([element])
        process = Thread(target=download_video, args=[link])
        process.start()

    def process_handler(self, progress_status):
        """Handler download status"""
        time.sleep(1)
        if progress_status['status'] == 'downloading' and 'total_bytes_estimate' in progress_status:
            video_download_percent = int(progress_status['downloaded_bytes'] * 100 / progress_status['total_bytes_estimate'])
            self.progress_percent = int(video_download_percent * 100 / 90)
        if progress_status['status'] == 'finished':
            self.progress_percent = 100

    def on_stop(self):
        self.save_setting()


class VideoThumbnail(ILeftBody, AsyncImage):
    pass


if __name__ == '__main__':
    YouTubeDownloader().run()
