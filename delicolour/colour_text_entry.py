import re
from delicolour import config
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango


class ColourTextEntry(Gtk.Entry):
    def __init__(self, maxlen):
        # parameters
        self._user_on_change = None
        self._clipboard_sel = Gdk.SELECTION_CLIPBOARD

        # build entry
        super().__init__()
        self.set_max_length(maxlen)
        self.modify_font(Pango.FontDescription('monospace bold 8'))
        self.set_width_chars(maxlen)
        self.set_max_width_chars(maxlen)
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
        if not self._match_input(new_text):
            self.stop_emission('insert-text')

    def _on_changed(self, editable):
        if not self._current_text_is_valid():
            # consider nothing changed
            return

        # notify user
        self._do_user_on_change()

    def _set_clipboard(self):
        txt = self._text_to_clipboard()
        Gtk.Clipboard.get(self._clipboard_sel).set_text(txt, -1)

    def _get_clipboard(self):
        txt = Gtk.Clipboard.get(self._clipboard_sel).wait_for_text()

        if txt is not None:
            txt = self._text_from_clipboard(txt)

        return txt

    def _on_cut(self, entry):
        self.stop_emission('cut-clipboard')

    def _on_copy(self, entry):
        if self._current_text_is_valid():
            self._set_clipboard()

        self.stop_emission('copy-clipboard')

    def _on_paste(self, entry):
        text = self._get_clipboard()

        if text is not None:
            self.set_text_no_emit(text)

            # notify user
            self._do_user_on_change()

        self.stop_emission('paste-clipboard')

    @property
    def colour(self):
        raise NotImplementedError()

    def set_colour_no_emit(self, colour):
        raise NotImplementedError()

    def set_text_no_emit(self, text):
        self.handler_block(self._changed_handler)
        self.set_text(self._get_real_text(text))
        self.handler_unblock(self._changed_handler)

    def on_change(self, cb):
        self._user_on_change = cb
