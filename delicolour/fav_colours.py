from delicolour.fav_colour import FavColour
from delicolour.colour import Colour
from gi.repository import Gtk, Gdk
from delicolour import config
import math


class FavColours(Gtk.Box):
    def __init__(self, max_height=(3 * config.MAIN_GUTTER_PX),
                 fav_colours_count=config.DEF_FAV_COLOURS_COUNT):
        super().__init__(spacing=config.MAIN_GUTTER_PX)
        self._fav_colours_count = fav_colours_count
        self._max_height = max_height
        self.connect('realize', self._on_realize)
        self._user_on_fav_colour_click = None

    def _get_size(self):
        alloc = self.get_allocation()

        return alloc.width, alloc.height

    def _on_realize(self, widget):
        width, height = self._get_size()
        colours_count = self._fav_colours_count
        self._fav_colours = []

        # remove gutters from total width
        width -= (colours_count - 1) * config.MAIN_GUTTER_PX

        # divide remaining width equally
        fav_colour_width = round(width / colours_count)

        # clip height if needed
        fav_colour_height = fav_colour_width

        if fav_colour_height > self._max_height:
            fav_colour_height = self._max_height

        for c in range(colours_count):
            fav_colour = FavColour(fav_colour_width, fav_colour_height)
            fav_colour.on_click(self._notify_on_fav_colour_click)
            self._fav_colours.append(fav_colour)
            self.pack_start(fav_colour, False, False, 0)
            fav_colour.show()

    @property
    def fav_colours(self):
        return self._fav_colours

    def _notify_on_fav_colour_click(self, event, fav_colour):
        if self._user_on_fav_colour_click:
            self._user_on_fav_colour_click(event, fav_colour)

    def on_fav_colour_click(self, cb):
        self._user_on_fav_colour_click = cb
