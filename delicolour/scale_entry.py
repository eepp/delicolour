import re
from delicolour import config
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango


class ScaleEntry(Gtk.HBox):
    def __init__(self, label, minval, maxval, step, r=0.15, g=0.15, b=0.15):
        # asked colour
        color = Gdk.Color(red=r * 65535, green=g * 65535, blue=b * 65535)

        # parameters
        self._minval = minval
        self._maxval = maxval
        self._step = step

        # label
        lbl = Gtk.Label()
        lbl.set_width_chars(2)
        lbl.set_markup('<b>{}</b>'.format(label))
        lbl.modify_fg(Gtk.StateType.NORMAL, color)

        # entry
        self._entry = Gtk.Entry()
        self._entry.modify_font(Pango.FontDescription('monospace bold 9'))
        self._entry.set_width_chars(4)
        self._entry.connect('insert-text', self._on_entry_insert_text)
        self._entry.connect('changed', self._on_entry_changed)
        self._entry.connect('button-press-event', self._on_entry_button_press)

        # scale
        adjustment = Gtk.Adjustment(0, minval, maxval, step, 0, 0)
        self._scale = Gtk.HScale()
        self._scale.set_adjustment(adjustment)
        self._scale.set_draw_value(False)
        self._scale.set_min_slider_size(15)
        self._scale.connect('change-value', self._on_scale_change_value)
        self._scale.set_can_focus(False)

        # hbox
        Gtk.HBox.__init__(self, spacing=config.MAIN_GUTTER_PX,
                          homogeneous=False)
        self.pack_start(lbl, False, True, 0)
        self.pack_start(self._scale, True, True, 0)
        self.pack_start(self._entry, False, True, 0)

        # user on change
        self._user_on_change = ScaleEntry.do_nothing

    @staticmethod
    def do_nothing():
        pass

    def set_value(self, value):
        if value < self._minval:
            value = self._minval
        elif value > self._maxval:
            value = self._maxval
        elif value is None:
            value = self.get_value()

        self._scale.set_value(value)
        self._entry.set_text(str(int(value)))

    def get_value(self):
        return self._scale.get_value()

    def _on_entry_button_press(self, entry, ev):
        pass
        #self._entry.select_region(0, len(self._entry.get_text()))

    def _on_entry_insert_text(self, entry, new_text, new_text_length,
                              position):
        if not re.search(r'^[0-9]*$', new_text):
            self._entry.stop_emission('insert-text')

    def _on_entry_changed(self, editable):
        text = self._entry.get_text()
        if len(text) == 0:
            # consider nothing changed
            return
        next_val = int(text)
        self.set_value(next_val)
        self._user_on_change()

    def _on_scale_change_value(self, scale, scroll, value):
        self.set_value(value)
        self._entry.grab_focus()
        self._user_on_change()

    def on_change(self, cb):
        self._user_on_change = cb

    def get_entry(self):
        return self._entry

    def get_scale(self):
        return self._scale
