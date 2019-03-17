# .-------------------.
# |      imports      |
# '-------------------'
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from lib.coreprocess import CoreProcess


# .-------------------.
# |      classes      |
# '-------------------'
class MainScreen(Screen):
    """
    Main Screen also Landing Screen, where user first launch the App.
    Receive user 'search keywords' or 'download URL' then process to the Detail Screen.
    """
    user_input = StringProperty('')
    processed_data = ObjectProperty(None)

    # Record user data then change to Detail Screen to process
    def change_screen(self, root, text=''):
        if text is not None:
            self.user_input = text
        self.process_request()
        root.transition.direction = 'left'
        root.current = 'Detail_Screen'
    
    def process_request(self):
        if self.user_input.startswith(("https", "http")):
            core_process.download_video(self.user_input)
        else:
            self.processed_data = core_process.search_by_keywords(self.user_input)

    def clear_cache(self):
        self.ids.data_text.text = ''


class DetailScreen(Screen):
    """
    Detail Screen receive user data from Main Screen then process base on data input.
    Result will show here for user.
    """
    resultText = ObjectProperty(None)
    
    def show_result(self):
        text = ''
        for link in self.resultText:
            text += link + "\n"
        self.ids.result_text.text = text


class ScreenControl(ScreenManager):
    """Dummy class for manager screens"""
    mainScreen = ObjectProperty(None)
    detailScreen = ObjectProperty(None)

    def update(self):
        self.detailScreen.resultText = self.mainScreen.processed_data
        self.detailScreen.show_result()


# .-------------------.
# |      global       |
# '-------------------'
core_process = CoreProcess()
buildKV = Builder.load_file("uimanager.kv")


class MyApp(App):
    """Dummy class for running app"""
    def build(self):
        return buildKV


if __name__ == '__main__':
    MyApp().run()
