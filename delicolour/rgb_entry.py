import re
from delicolour import config
from delicolour.colour import Colour
from delicolour.colour_text_entry import ColourTextEntry
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango


class RgbEntry(ColourTextEntry):
    def __init__(self):
        ColourTextEntry.__init__(self, 18)

    @staticmethod
    def _text_is_valid(text):
        text = text.lower()
        return re.search(r'^rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$', text)

    def _current_text_is_valid(self):
        return RgbEntry._text_is_valid(self.get_text())

    def _match_input(self, text):
        text = text.lower()
        return re.search(r'^[ rgb()\,0-9]*$', text)

    def _text_to_clipboard(self):
        return self.get_text().lower()

    def _text_from_clipboard(self, text):
        text = text.lower().strip()
        if self._text_is_valid(text):
            return text

        return None

    def _get_real_text(self, text):
        return text.lower()

    def get_colour(self):
        return Colour.from_css_rgb(self.get_text())

    def set_colour_no_emit(self, colour):
        self.set_text_no_emit(colour.get_css_rgb())
