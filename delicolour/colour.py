import re
from colormath.color_objects import RGBColor
from colormath.color_objects import HSVColor
from colormath.color_objects import HSLColor


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
        hex_str = hex_str.strip()
        if len(hex_str) == 3:
            hex_str = '{r}{r}{g}{g}{b}{b}'.format(r=hex_str[0],
                                                   g=hex_str[1],
                                                   b=hex_str[2])
        if len(hex_str) != 6:
            return
        self._rgb_color.set_from_rgb_hex(hex_str)
        self._update_hsv_from_rgb()

    def inc_light(self, val):
        hsl = self._hsv_color.convert_to('hsl')
        light = hsl.hsl_l
        light += val
        if light > 1:
            light = 1
        hsl.hsl_l = light
        self._hsv_color = hsl.convert_to('hsv')
        self._update_rgb_from_hsv()

    def dec_light(self, val):
        hsl = self._hsv_color.convert_to('hsl')
        light = hsl.hsl_l
        light -= val
        if light < 0:
            light = 0
        hsl.hsl_l = light
        self._hsv_color = hsl.convert_to('hsv')
        self._update_rgb_from_hsv()

    def inc_sat(self, val):
        sat = self._hsv_color.hsv_s
        sat += val
        if sat > 1:
            sat = 1
        self._hsv_color.hsv_s = sat
        self._update_rgb_from_hsv()

    def dec_sat(self, val):
        sat = self._hsv_color.hsv_s
        sat -= val
        if sat < 0:
            sat = 0
        self._hsv_color.hsv_s = sat
        self._update_rgb_from_hsv()

    @staticmethod
    def _rgb_in_range(r, g, b):
        good = True
        for val in [r, g, b]:
            good &= (val >= 0 and val <= 255)

        return good

    def set_css_rgb(self, rgb_str):
        rgb_str = rgb_str.strip()
        print(rgb_str)
        m = re.match(r'^rgb\s*\(\s*(\d+)\s*\,\s*(\d+)\s*\,\s*(\d+)\s*\)$', rgb_str)
        if not m:
            return
        print('match!')
        r = int(m.group(1))
        g = int(m.group(2))
        b = int(m.group(3))
        if not Colour._rgb_in_range(r, g, b):
            return

        self.set_rgb(r, g, b)

    def get_css_rgb(self):
        r, g, b = self.get_rgb()
        return 'rgb({}, {}, {})'.format(r, g, b)

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

    @staticmethod
    def from_css_rgb(rgb_str):
        c = Colour()
        c.set_css_rgb(rgb_str)

        return c

