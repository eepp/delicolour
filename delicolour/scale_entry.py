import re
from delicolour import config
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango


class ScaleEntry(Gtk.HBox):
    def __init__(self, label, minval, maxval, page_incr, r=0.15, g=0.15, b=0.15):
        # asked colour
        color = Gdk.Color(red=r * 65535, green=g * 65535, blue=b * 65535)

        # parameters
        self._minval = minval
        self._maxval = maxval
        self._page_incr = page_incr

        # label
        lbl = Gtk.Label()
        lbl.set_width_chars(2)
        lbl.set_markup('<b>{}</b>'.format(label))
        lbl.modify_fg(Gtk.StateType.NORMAL, color)
        self._label = label

        # entry
        self._entry = Gtk.Entry()
        self._entry.modify_font(Pango.FontDescription('monospace bold 9'))
        self._entry.set_width_chars(4)
        self._entry.connect('insert-text', self._on_entry_insert_text)
        self._entry.connect('scroll-event', self._on_entry_scroll_event)
        self._entry_changed_handler = self._entry.connect('changed', self._on_entry_changed)


        # scale
        adjustment = Gtk.Adjustment(0, minval, maxval, 1, page_incr, 0)
        self._scale = Gtk.HScale()
        self._scale.set_adjustment(adjustment)
        self._scale.set_draw_value(False)
        self._scale.set_min_slider_size(15)
        self._scale.connect('change-value', self._on_scale_change_value)
        self._scale.set_can_focus(False)
        self._scale.set_round_digits(0)
        self._scale.set_digits(0)

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

    def set_page_incr(self, page_incr):
        self._page_incr = page_incr
        ajd = self._scale.get_adjustment()
        ajd.set_page_increment(page_incr)
        self._scale.set_adjustment(ajd)

    def _get_normalized_value(self, value):
        if value < self._minval:
            return self._minval
        elif value > self._maxval:
            return self._maxval
        elif value is None:
            return self.get_value()
        else:
            return value

    def _set_scale_value_no_emit(self, value):
        self._scale.set_value(value)

    def _set_entry_value_no_emit(self, value):
        txt = str(round(value))
        self._entry.handler_block(self._entry_changed_handler)
        self._entry.set_text(txt)
        self._entry.handler_unblock(self._entry_changed_handler)

    def set_value_no_emit(self, value):
        value = self._get_normalized_value(value)
        self._set_entry_value_no_emit(value)
        self._set_scale_value_no_emit(value)

    def get_value(self):
        return self._scale.get_value()

    def _on_entry_insert_text(self, entry, new_text, new_text_length,
                              position):
        if not re.search(r'^[0-9]*$', new_text):
            self._entry.stop_emission('insert-text')

    def _on_entry_changed(self, editable):
        text = self._entry.get_text()
        if len(text) == 0:
            # consider nothing changed
            return

        # value
        next_val = self._get_normalized_value(int(text))

        # set scale value
        self._set_scale_value_no_emit(next_val)

        # notify user
        self._user_on_change()

    def _on_entry_scroll_event(self, widget, ev):
        print(ev)

    def _on_scale_change_value(self, scale, scroll, value):
        print(value)
        print(scroll)

        # value
        value = self._get_normalized_value(value)

        # set scale value
        self._set_scale_value_no_emit(value)

        # set entry value
        self._set_entry_value_no_emit(value)

        # notify user
        self._user_on_change()

        return True

    def on_change(self, cb):
        self._user_on_change = cb

    def get_entry(self):
        return self._entry

    def get_scale(self):
        return self._scale

    def set_focus(self):
        self._entry.grab_focus()
