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
        return int(c.rgb_r), int(c.rgb_g), int(c.rgb_b)

    def get_hsv(self):
        c = self._hsv_color
        return c.hsv_h, c.hsv_s, c.hsv_v

    def get_hex(self):
        r, g, b = self.get_rgb()
        return '{:02x}{:02x}{:02x}'.format(r, g, b)

    def set_hex(self, hex_str):
        if len(hex_str) == 3:
            hex_str = '{r}{r}{g}{g}{b}{b}'.format(r=hex_str[0],
                                                   g=hex_str[1],
                                                   b=hex_str[2])
        if len(hex_str) != 6:
            return
        self._rgb_color.set_from_rgb_hex(hex_str)
        self._update_hsv_from_rgb()

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

    @staticmethod
    def from_hex(hex_str):
        c = Colour()
        c.set_hex(hex_str)

        return c
