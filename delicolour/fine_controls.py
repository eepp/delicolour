import re
from delicolour import config
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango


class FineControls(Gtk.Box):
    def __init__(self, minval, maxval):
        # parameters
        self._minval = minval
        self._maxval = maxval
        self._user_on_inc_light = None
        self._user_on_dec_light = None
        self._user_on_inc_sat = None
        self._user_on_dec_sat = None
        self._user_on_incr_change = None

        # parent box
        super().__init__(self, spacing=0, homogeneous=False)
        self.set_orientation(Gtk.Orientation.HORIZONTAL)

        # controls
        self._init_controls()

    @staticmethod
    def _new_fine_control_btn(img_filename, tooltip_text):
        img = Gtk.Image()
        img.set_from_file(img_filename)
        btn = Gtk.Button()
        btn.set_tooltip_text(tooltip_text)
        btn.add(img)

        return btn

    def _init_controls(self):
        # buttons
        self._inc_light = FineControls._new_fine_control_btn('res/sun-24.png',
                                                             'Increase lightness')
        self._dec_light = FineControls._new_fine_control_btn('res/moon-24.png',
                                                             'Decrease lightness')
        self._inc_sat = FineControls._new_fine_control_btn('res/sat-24.png',
                                                           'Increase saturation')
        self._dec_sat = FineControls._new_fine_control_btn('res/desat-24.png',
                                                           'Decrease saturation')

        # set callbacks
        self._inc_light.connect('clicked', self._on_inc_light_clicked)
        self._dec_light.connect('clicked', self._on_dec_light_clicked)
        self._inc_sat.connect('clicked', self._on_inc_sat_clicked)
        self._dec_sat.connect('clicked', self._on_dec_sat_clicked)

        # alignments
        a_pad_left = Gtk.Alignment()
        a_pad_left.set_padding(0, 0, config.MAIN_GUTTER_PX, 0)
        a_pad_left.add(self._dec_light)

        # pack into box
        self.pack_end(self._inc_light, False, True, 0)
        self.pack_end(a_pad_left, False, True, 0)
        self.pack_end(self._inc_sat, False, True, 0)
        self.pack_end(self._dec_sat, False, True, 0)

        # spinner
        adj = Gtk.Adjustment(value=1, lower=self._minval, upper=self._maxval,
                             step_incr=1, page_incr=1)
        self._spin = Gtk.SpinButton()
        self._spin.set_tooltip_text('Fine controls increment value')
        self._spin.set_adjustment(adj)
        self._spin.modify_font(Pango.FontDescription('monospace bold 8'))
        self._spin.set_width_chars(3)
        self._spin.set_max_width_chars(3)
        self._on_spin_changed_handler = self._spin.connect('changed', self._on_spin_changed)
        self.pack_start(self._spin, False, True, 0)

    def _on_inc_light_clicked(self, btn):
        if self._user_on_inc_light:
            self._user_on_inc_light()

    def _on_dec_light_clicked(self, btn):
        if self._user_on_dec_light:
            self._user_on_dec_light()

    def _on_inc_sat_clicked(self, btn):
        if self._user_on_inc_sat:
            self._user_on_inc_sat()

    def _on_dec_sat_clicked(self, btn):
        if self._user_on_dec_sat:
            self._user_on_dec_sat()

    def _on_spin_changed(self, edit):
        text = edit.get_text()

        try:
            orig_val = int(text)
        except:
            self.set_incr_value_no_emit(self._minval)
            return

        val = orig_val

        if val < self._minval:
            val = self._minval
        elif val > self._maxval:
            val = self._maxval

        if val != orig_val:
            self.set_incr_value_no_emit(val)

        # notify user
        if self._user_on_incr_change:
            self._user_on_incr_change()

    def set_incr_value_no_emit(self, val):
        self._spin.handler_block(self._on_spin_changed_handler)
        self._spin.set_value(val)
        self._spin.handler_unblock(self._on_spin_changed_handler)

    def get_incr_value(self):
        return self._spin.get_value_as_int()

    def on_inc_light(self, cb):
        self._user_on_inc_light = cb

    def on_dec_light(self, cb):
        self._user_on_dec_light = cb

    def on_inc_sat(self, cb):
        self._user_on_inc_sat = cb

    def on_dec_sat(self, cb):
        self._user_on_dec_sat = cb

    def on_incr_change(self, cb):
        self._user_on_incr_change = cb
