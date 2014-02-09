from colormath.color_objects import RGBColor


class Colour:
    def __init__(self):
        self.set_rgb(0, 0, 0)

    def set_rgb(self, r, g, b):
        self._r = r;
        self._g = g;
        self._b = b;

    def get_rgb(self):
        return self._r, self._g, self._b

    @staticmethod
    def from_rgb(r, g, b):
        c = Colour()
        c.set_rgb(r, g, b)

        return c
