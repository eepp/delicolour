import re
from colormath.color_objects import AdobeRGBColor
from colormath.color_objects import HSVColor
from colormath.color_objects import HSLColor
from colormath.color_conversions import convert_color

class Colour:
    def __init__(self, r=0, g=0, b=0):
        self.set_rgb(r, g, b)

    def __repr__(self):
        r, g, b = self.rgb

        return 'Colour({}, {}, {})'.format(r, g, b)

    def set_rgb(self, r, g, b):
        self._set_rgb_color(AdobeRGBColor(r, g, b, True))

    def set_r(self, r):
        self._rgb_color.rgb_r = r
        self._update_hsv_from_rgb()

    def set_g(self, g):
        self._rgb_color.rgb_g = g
        self._update_hsv_from_rgb()

    def set_b(self, b):
        self._rgb_color.rgb_b = b
        self._update_hsv_from_rgb()

    def set_hsv(self, h, s, v):
        self._set_hsv_color(HSVColor(h, s, v))

    def _update_rgb_from_hsv(self):
        self._rgb_color = convert_color(self._hsv_color, AdobeRGBColor)

    def _update_hsv_from_rgb(self):
        self._hsv_color = convert_color(self._rgb_color, HSVColor)

    @property
    def rgb(self):
        return self._rgb_color.get_upscaled_value_tuple()

    @property
    def hsv(self):
        c = self._hsv_color

        return c.hsv_h, c.hsv_s, c.hsv_v

    @property
    def hex(self):
        r, g, b = self.rgb

        return '{:02x}{:02x}{:02x}'.format(r, g, b)

    def set_from_hex(self, hex_str):
        hex_str = hex_str.strip()

        if hex_str.startswith('#'):
            hex_str = hex_str[1:]

        if len(hex_str) == 3:
            hex_str = '{r}{r}{g}{g}{b}{b}'.format(r=hex_str[0],
                                                  g=hex_str[1],
                                                  b=hex_str[2])

        if len(hex_str) != 6:
            return

        color = AdobeRGBColor.new_from_rgb_hex(hex_str)
        self._set_rgb_color(color)

    def _set_hsv_color(self, hsv):
        self._hsv_color = hsv
        self._update_rgb_from_hsv()

    def _set_rgb_color(self, rgb):
        self._rgb_color = rgb
        self._update_hsv_from_rgb()

    @property
    def _hsl_color(self):
        return convert_color(self._hsv_color, HSLColor)

    def inc_light(self, val):
        hsl = self._hsl_color
        light = hsl.hsl_l
        light += val

        # clip
        if light > 1:
            light = 1

        hsl.hsl_l = light
        self._set_hsv_color(convert_color(hsl, HSVColor))

    def dec_light(self, val):
        hsl = self._hsl_color
        light = hsl.hsl_l
        light -= val

        # clip
        if light < 0:
            light = 0

        hsl.hsl_l = light
        self._set_hsv_color(convert_color(hsl, HSVColor))

    def inc_sat(self, val):
        sat = self._hsv_color.hsv_s
        sat += val

        # clip
        if sat > 1:
            sat = 1

        self._hsv_color.hsv_s = sat
        self._update_rgb_from_hsv()

    def dec_sat(self, val):
        sat = self._hsv_color.hsv_s
        sat -= val

        # clip
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

    def set_from_css_rgb(self, rgb_str):
        rgb_str = rgb_str.strip()
        m = re.match(r'^rgb\s*\(\s*(\d+)\s*\,\s*(\d+)\s*\,\s*(\d+)\s*\)$', rgb_str)

        if not m:
            return

        r = int(m.group(1))
        g = int(m.group(2))
        b = int(m.group(3))

        if not Colour._rgb_in_range(r, g, b):
            return

        self.set_rgb(r, g, b)

    def get_css_rgb(self):
        r, g, b = self.rgb

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
        c.set_from_hex(hex_str)

        return c

    @staticmethod
    def from_css_rgb(rgb_str):
        c = Colour()
        c.set_from_css_rgb(rgb_str)

        return c

    def copy(self):
        r, g, b = self.rgb

        return Colour.from_rgb(r, g, b)
