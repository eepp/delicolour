import re
from delicolour import config
from delicolour.colour import Colour
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango


class HexEntry(Gtk.Entry):
    def __init__(self, lower=True):
        # parameters
        self._lower = lower
        self._user_on_change = None

        # build entry
        Gtk.Entry.__init__(self)
        self.set_max_length(6)
        self.modify_font(Pango.FontDescription('monospace bold 8'))
        self.set_width_chars(6)
        self.connect('insert-text', self._on_insert_text)
        self._changed_handler = self.connect('changed', self._on_changed)

    def _do_user_on_change(self):
        if self._user_on_change:
            self._user_on_change()

    def _on_insert_text(self, entry, new_text, new_text_length,
                              position):
        if not re.search(r'^[0-9a-fA-F]*$', new_text):
            self.stop_emission('insert-text')

    def _on_changed(self, editable):
        text = self.get_text()
        if len(text) not in [3, 6]:
            # consider nothing changed
            return

        # notify user
        self._do_user_on_change()

    def get_colour(self):
        return Colour.from_hex(self.get_text())

    def set_colour_no_emit(self, colour):
        self.handler_block(self._changed_handler)
        text = colour.get_hex().upper()
        if self._lower:
            text = text.lower()
        self.set_text(text)
        self.handler_unblock(self._changed_handler)

    def on_change(self, cb):
        self._user_on_change = cb
