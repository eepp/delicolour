from delicolour.colour import Colour


class AppModel:
    def __init__(self):
        self._sel = 1

    @property
    def colour(self):
        if self.sel == 1:
            return self.colour_l
        else:
            return self.colour_r

    @colour.setter
    def colour(self, colour):
        copy = colour.copy()

        if self.sel == 1:
            self.colour_l = copy
        else:
            self.colour_r = copy

    @property
    def sel(self):
        return self._sel

    @sel.setter
    def sel(self, sel):
        self._sel = sel

    @staticmethod
    def get_default():
        model = AppModel()
        model.colour_l = Colour.from_rgb(255, 255, 255)
        model.colour_r = Colour.from_rgb(0, 0, 0)
        model.css_hex_copy_hash = True
        model.css_hex_lower = True
        model.fine_incr = 1

        return model

