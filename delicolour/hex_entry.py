import re
from delicolour import config
from delicolour.colour import Colour
from delicolour.colour_text_entry import ColourTextEntry
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango


class HexEntry(ColourTextEntry):
    def __init__(self, lower=True, copy_hash=True):
        # parameters
        self._lower = lower
        self._copy_hash = copy_hash

        # build parent
        ColourTextEntry.__init__(self, 6)

    def _text_len_is_valid(self, text):
        return len(text) in [3, 6]

    def _current_text_is_valid(self):
        text = self.get_text()
        return self._text_len_is_valid(text)

    def _match_input(self, text):
        return re.search(r'^[0-9a-fA-F]*$', text)

    def _text_to_clipboard(self):
        text = self.get_text()
        if self._copy_hash:
            text = '#{}'.format(text)

        return text

    def _text_from_clipboard(self, text):
        text = text.strip()
        if text.startswith('#'):
            text = text[1:]
        if self._text_len_is_valid(text):
            return text

        return None

    def _on_changed(self, editable):
        text = self.get_text()
        if len(text) not in [3, 6]:
            # consider nothing changed
            return

        # notify user
        self._do_user_on_change()

    def _get_real_text(self, text):
        text = text.upper()
        if self._lower:
            text = text.lower()

        return text

    def set_lower(self, lower):
        self._lower = lower

    def set_copy_hash(self, copy_hash):
        self._copy_hash = copy_hash

    def get_colour(self):
        return Colour.from_hex(self.get_text())

    def set_colour_no_emit(self, colour):
        self.set_text_no_emit(colour.get_hex())
