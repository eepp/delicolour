import re
from delicolour import config
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango
from delicolour.adjustment_controls import AdjustmentControls


class FineControls(Gtk.Box):
    def __init__(self, minval, maxval):
        # parameters
        self._minval = minval
        self._maxval = maxval
        self._user_on_inc_light = None
        self._user_on_dec_light = None
        self._user_on_inc_sat = None
        self._user_on_dec_sat = None

        # parent box
        super().__init__(spacing=0, homogeneous=False)
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
        self.pack_end(self._inc_light, False, False, 0)
        self.pack_end(a_pad_left, False, False, 0)
        self.pack_end(self._inc_sat, False, False, 0)
        self.pack_end(self._dec_sat, False, False, 0)

        # adjustment controls
        self._adj = AdjustmentControls(1, 15)
        self.pack_start(self._adj, False, False, 0)

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

    @property
    def incr_value(self):
        return self._adj.value

    def on_inc_light(self, cb):
        self._user_on_inc_light = cb

    def on_dec_light(self, cb):
        self._user_on_dec_light = cb

    def on_inc_sat(self, cb):
        self._user_on_inc_sat = cb

    def on_dec_sat(self, cb):
        self._user_on_dec_sat = cb

    def on_incr_change(self, cb):
        self._adj.on_incr_change(cb)
