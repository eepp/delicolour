import re
from delicolour import config
from delicolour.colour import Colour
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango


class HexEntry(Gtk.Entry):
    def __init__(self, lower=True, copy_hash=True):
        # parameters
        self._lower = lower
        self._user_on_change = None
        self._copy_hash = copy_hash
        self._clipboard_sel = Gdk.SELECTION_CLIPBOARD

        # build entry
        Gtk.Entry.__init__(self)
        self.set_max_length(6)
        self.modify_font(Pango.FontDescription('monospace bold 8'))
        self.set_width_chars(6)
        self.connect('insert-text', self._on_insert_text)
        self._changed_handler = self.connect('changed', self._on_changed)
        self.connect('cut-clipboard', self._on_cut)
        self.connect('copy-clipboard', self._on_copy)
        self.connect('paste-clipboard', self._on_paste)

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

    def _set_clipboard(self, txt):
        Gtk.Clipboard.get(self._clipboard_sel).set_text(txt, -1)

    def _get_clipboard(self):
        return Gtk.Clipboard.get(self._clipboard_sel).wait_for_text()

    def _on_cut(self, entry):
        self.stop_emission('cut-clipboard')

    def _on_copy(self, entry):
        text = self.get_text()
        if len(text) in [3, 6]:
            if self._copy_hash:
                text = '#{}'.format(text)
            self._set_clipboard(text)
        self.stop_emission('copy-clipboard')

    def _on_paste(self, entry):
        text = self._get_clipboard()
        if text is not None:
            if text.startswith('#'):
                text = text[1:]
            if len(text) in [3, 6]:
                self.set_text_no_emit(text)

                # notify user
                self._do_user_on_change()
        self.stop_emission('paste-clipboard')

    def set_lower(self, lower):
        self._lower = lower

    def set_copy_hash(self, copy_hash):
        self._copy_hash = copy_hash

    def get_colour(self):
        return Colour.from_hex(self.get_text())

    def set_colour_no_emit(self, colour):
        self.set_text_no_emit(colour.get_hex())

    def set_text_no_emit(self, text):
        text = text.upper()
        if self._lower:
            text = text.lower()
        self.handler_block(self._changed_handler)
        self.set_text(text)
        self.handler_unblock(self._changed_handler)

    def on_change(self, cb):
        self._user_on_change = cb
