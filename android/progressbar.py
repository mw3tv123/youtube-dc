# -*- coding: utf-8 -*-

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ListProperty, OptionProperty, BooleanProperty,NumericProperty,StringProperty
from kivy.utils import get_color_from_hex
from kivy.uix.progressbar import ProgressBar

from kivymd.color_definitions import colors
from kivymd.theming import ThemableBehavior


Builder.load_string('''
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import MDLabel kivymd.label.MDLabel
<MDProgressBar>:
    canvas:
        Clear
        Color:
            rgba: self.theme_cls.divider_color
        Rectangle:
            size: (self.width * 0.6, dp(18)) if self.orientation == 'horizontal' else (dp(18), self.height - dp(8))
            pos: (self.x + self.width * 0.2, self.center_y) if self.orientation == 'horizontal' \
                                                            else (self.center_x + dp(24), self.y)
        Color:
            rgba: get_color_from_hex(self.rgbr)
        Rectangle:
            size: (self.width * self.value_normalized * 0.6, sp(18)) if self.orientation == 'horizontal' \
                                                                     else (sp(18), self.height * self.value_normalized)
            pos: (self.width * 0.6 * (1 - self.value_normalized) + self.x + self.width * 0.2 \
                if self.reversed else self.x + self.width * 0.2, self.center_y) \
                if self.orientation == 'horizontal' \
                else (self.center_x + dp(24), self.height * (1 - self.value_normalized) + self.y \
                if self.reversed else self.y)
''')


class MDProgressBar(ThemableBehavior, ProgressBar):
    reversed = BooleanProperty(False)
    ''' Reverse the direction the progressbar moves. '''
    orientation = OptionProperty('horizontal', options=['horizontal', 'vertical'])
    ''' Orientation of progressbar'''
    rgbr = StringProperty("FF0000")

    def on_rgbr(self, instance, value):
        r1, r2 = 153, 255
        g1, g2 = 255, 0
        b1, b2 = 0, 0
        r = int((r1 * self.value + r2 * (100 - self.value)) / 100)
        g = int((g1 * self.value + g2 * (100 - self.value)) / 100)
        b = int((b1 * self.value + b2 * (100 - self.value)) / 100)

        self.rgbr = hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2)

    def on_value(self, instance, value):
        r1, r2 = 255, 153
        g1, g2 = 0, 255
        b1, b2 = 0, 0
        r = int((r1 * self.value + r2 * (100 - self.value)) / 100)
        g = int((g1 * self.value + g2 * (100 - self.value)) / 100)
        b = int((b1 * self.value + b2 * (100 - self.value)) / 100)

        self.rgbr = hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2)