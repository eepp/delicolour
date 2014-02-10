from colormath.color_objects import RGBColor
from colormath.color_objects import HSVColor


class Colour:
    def __init__(self):
        self.set_rgb(0, 0, 0)

    def set_rgb(self, r, g, b):
        self._rgb_color = RGBColor(r, g, b)
        self._update_hsv_from_rgb()

    def set_hsv(self, h, s, v):
        self._hsv_color = HSVColor(h, s, v)
        self._update_rgb_from_hsv()

    def _update_rgb_from_hsv(self):
        self._rgb_color = self._hsv_color.convert_to('rgb')

    def _update_hsv_from_rgb(self):
        self._hsv_color = self._rgb_color.convert_to('hsv')

    def get_rgb(self):
        c = self._rgb_color
        return c.rgb_r, c.rgb_g, c.rgb_b

    def get_hsv(self):
        c = self._hsv_color
        return c.hsv_h, c.hsv_s, c.hsv_v

    @staticmethod
    def from_rgb(r, g, b):
        c = Colour()
        c.set_rgb(r, g, b)

        return c

    @staticmethod
    def from_hsv(h, s, v):
        c = Colour()
        c.set_hsv(h, s, v)

        return c
