from delicolour import config
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango


class AdjustmentControls(Gtk.Box):
    def __init__(self, minval, maxval, init_adj):
        # user callbacks
        self._user_on_incr_change = None

        # parameters
        self._minval = minval
        self._maxval = maxval

        # parent box
        super().__init__(spacing=0, homogeneous=False)
        self.set_orientation(Gtk.Orientation.HORIZONTAL)

        # controls
        self._init_controls()
        self._value_lbl.set_text(str(init_adj))

    @staticmethod
    def _new_btn(label, tooltip_text):
        btn = Gtk.Button(label=label)
        btn.set_tooltip_text(tooltip_text)
        btn.set_size_request(30, -1)
        btn.set_valign(Gtk.Align.CENTER)
        my_style_provider = Gtk.CssProvider()
        my_style_provider.load_from_data(b'GtkWidget {padding: 3px;}')
        style_context = btn.get_style_context()
        style_context.add_provider(my_style_provider,
                                   Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        return btn

    def _init_controls(self):
        # label
        self._value_lbl = Gtk.Label()
        self._value_lbl.modify_font(Pango.FontDescription('sans-serif bold 8'))
        self._value_lbl.set_text(str(self._minval))
        self._value_lbl.set_width_chars(2)
        self._value_lbl.set_alignment(0, 0.5)
        self._value_lbl.set_tooltip_text('Fine-tuning increment')

        # buttons
        self._dec_btn = self._new_btn('-', 'Decrement fine-tuning increment')
        self._inc_btn = self._new_btn('+', 'Increment fine-tuning increment')

        # set callbacks
        self._dec_btn.connect('clicked', self._on_dec)
        self._inc_btn.connect('clicked', self._on_inc)

        # alignments
        a_pad_left = Gtk.Alignment()
        a_pad_left.set_padding(0, 0, config.MAIN_GUTTER_PX, 0)
        a_pad_left.add(self._dec_btn)

        # pack into box
        self.pack_start(self._value_lbl, False, False, 0)
        self.pack_start(a_pad_left, False, False, 0)
        self.pack_start(self._inc_btn, False, False, 0)

    def _on_incr_change(self):
        if self._user_on_incr_change:
            self._user_on_incr_change()

    def _on_inc(self, btn):
        val = self.value

        if val == self._maxval:
            return

        val += 1
        self._value_lbl.set_text(str(val))
        self._on_incr_change()

    def _on_dec(self, btn):
        val = self.value

        if val == self._minval:
            return

        val -= 1
        self._value_lbl.set_text(str(val))
        self._on_incr_change()

    @property
    def value(self):
        return int(self._value_lbl.get_text())

    def on_incr_change(self, cb):
        self._user_on_incr_change = cb
