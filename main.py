# .-------------------.
# |      imports      |
# '-------------------'
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen

# from lib.coreprocess import CoreProcess

# import youtube_dl


# .---------------.
# |    classes    |
# '---------------'
class MainScreen(Screen):
    """
    Main Screen also Landing Screen, where user first launch the App.
    Receive user 'search keywords' or 'download URL' then process to the Detail Screen.
    """
    user_input = StringProperty('')

    # Record user data then change to Detail Screen to process
    def change_screen(self, root, text=''):
        if text is not None:
            self.user_input = text
        root.transition.direction = 'left'
        root.current = 'Detail_Screen'


class DetailScreen(Screen):
    """
    Detail Screen receive user data from Main Screen then process base on data input.
    Result will show here for user.
    """
    def on_enter(self, *args):
        pass


class ScreenControl(ScreenManager):
    """Dummy class for manager screens"""
    mainScreen = ObjectProperty(None)
    detailScreen = ObjectProperty(None)


# Import Kivy file for create UI
buildKV = Builder.load_file("uimanager.kv")


class MyApp(App):
    """Dummy class for running app"""
    def build(self):
        return buildKV


if __name__ == '__main__':
    MyApp().run()
