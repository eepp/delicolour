import re
from delicolour import config
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango


_re_key_press = re.compile(r'[a-zA-Z]')


class ScaleEntry(Gtk.Box):
    def __init__(self, label, minval, maxval, page_incr,
                 r=config.TEXT_COLOUR_R, g=config.TEXT_COLOUR_G,
                 b=config.TEXT_COLOUR_B, wrap=False):
        # asked colour
        color = Gdk.Color(red=r * 65535, green=g * 65535, blue=b * 65535)

        # parameters
        self._minval = minval
        self._maxval = maxval
        self._page_incr = page_incr
        self._wrap = wrap
        self._user_on_change = None
        self._user_on_key_press = None

        # label
        lbl = Gtk.Label()
        lbl.modify_font(Pango.FontDescription('sans-serif bold 8'))
        lbl.set_width_chars(2)
        lbl.set_text(label)
        lbl.modify_fg(Gtk.StateType.NORMAL, color)
        self._label = label

        # entry
        self._entry = Gtk.Entry()
        self._entry.set_max_length(3)
        self._entry.modify_font(Pango.FontDescription('monospace bold 8'))
        self._entry.set_width_chars(3)
        self._entry.set_max_width_chars(3)
        self._entry.set_alignment(1)
        self._entry.add_events(Gdk.EventMask.SCROLL_MASK | Gdk.EventMask.SMOOTH_SCROLL_MASK)
        self._entry.connect('insert-text', self._on_entry_insert_text)
        self._entry.connect('scroll-event', self._on_entry_scroll_event)
        self._entry.connect('key-press-event', self._on_entry_key_press)
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
        super().__init__(spacing=config.MAIN_GUTTER_PX, homogeneous=False)
        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.pack_start(lbl, False, False, 0)
        self.pack_start(self._scale, True, True, 0)
        self.pack_start(self._entry, False, False, 0)

    def set_page_incr(self, page_incr):
        self._page_incr = page_incr
        ajd = self._scale.get_adjustment()
        ajd.set_page_increment(page_incr)
        self._scale.set_adjustment(ajd)

    def _do_user_on_change(self):
        if self._user_on_change:
            self._user_on_change()

    def _do_user_on_key_press(self, key_name):
        if self._user_on_key_press:
            self._user_on_key_press(key_name)

    def _get_normalized_value(self, value):
        if value is None:
            value = self.value

        value = int(value)

        # clip?
        if value < self._minval:
            return self._minval
        elif value > self._maxval:
            return self._maxval
        elif value is None:
            return self.value
        else:
            return value

    def _set_scale_value_no_emit(self, value):
        self._scale.set_value(value)

    def _set_entry_value_no_emit(self, value):
        txt = str(round(value))
        self._entry.handler_block(self._entry_changed_handler)
        self._entry.set_text(txt)
        self._entry.handler_unblock(self._entry_changed_handler)

    def _set_ctrl_values_no_emit(self, value):
        value = self._get_normalized_value(value)
        self._set_entry_value_no_emit(value)
        self._set_scale_value_no_emit(value)

    def set_value_no_emit(self, value):
        self._set_ctrl_values_no_emit(value)

    @property
    def value(self):
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
        next_val = self._get_normalized_value(round(float(text)))

        # set scale value
        self._set_scale_value_no_emit(next_val)

        # notify user
        self._do_user_on_change()

    def _on_entry_scroll_event(self, widget, ev):
        value = self.value
        y_scroll = ev.get_scroll_deltas()[2]

        if y_scroll < 0:
            value += self._page_incr
        elif y_scroll > 0:
            value -= self._page_incr

        # wrap?
        if self._wrap:
            value = (value % (self._maxval + 1 - self._minval)) + self._minval

        # set control values
        self._set_ctrl_values_no_emit(value)

        # notify user
        self._do_user_on_change()

    def _on_entry_key_press(self, widget, event):
        key_name = Gdk.keyval_name(event.keyval)

        if _re_key_press.match(key_name):
            self._do_user_on_key_press(key_name)

    def _on_scale_change_value(self, scale, scroll, value):
        # value
        value = self._get_normalized_value(value)

        # set scale value
        self._set_scale_value_no_emit(value)

        # set entry value
        self._set_entry_value_no_emit(value)

        # notify user
        self._do_user_on_change()

        return True

    def on_change(self, cb):
        self._user_on_change = cb

    def on_key_press(self, cb):
        self._user_on_key_press = cb

    def get_entry(self):
        return self._entry

    def get_scale(self):
        return self._scale

    def set_focus(self):
        self._entry.grab_focus()
