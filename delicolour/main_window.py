from delicolour import config
from delicolour.app_model import AppModel
from delicolour.scale_entry import ScaleEntry
from delicolour.big_colour import BigColour
from delicolour.hex_entry import HexEntry
from delicolour.rgb_entry import RgbEntry
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="delicolour")
        self._make_me_nice()
        self._init_main_box()
        self._model = AppModel.get_default()
        self._update_view('init')

    def _make_me_nice(self):
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(config.MAIN_GUTTER_PX)
        self.set_resizable(False)

    def _init_main_box(self):
        self._main_box = Gtk.VBox(spacing=config.MAIN_GUTTER_PX,
                                  homogeneous=False)
        self._main_box.set_size_request(320, 0)
        self.add(self._main_box)
        self._init_all()

    def _init_big_colour(self):
        self._big_colour = BigColour()
        self._main_box.pack_start(self._big_colour, True, True, 0)

    @staticmethod
    def _new_fine_control_btn(img_filename, tooltip_text):
        img = Gtk.Image()
        img.set_from_file(img_filename)
        btn = Gtk.Button()
        btn.set_tooltip_text(tooltip_text)
        btn.add(img)

        return btn

    def _init_fine_colour_controls(self):
        # buttons
        self._inc_light = MainWindow._new_fine_control_btn('res/sun-24.png',
                                                           'Increase lightness')
        self._dec_light = MainWindow._new_fine_control_btn('res/moon-24.png',
                                                           'Decrease lightness')
        self._inc_sat = MainWindow._new_fine_control_btn('res/sat-24.png',
                                                         'Increase saturation')
        self._dec_sat = MainWindow._new_fine_control_btn('res/desat-24.png',
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

        # box
        box = Gtk.HBox(spacing=0, homogeneous=False)

        # pack into box
        box.pack_end(self._inc_light, False, True, 0)
        box.pack_end(a_pad_left, False, True, 0)
        box.pack_end(self._inc_sat, False, True, 0)
        box.pack_end(self._dec_sat, False, True, 0)

        # add to proper vbox
        self._main_box.pack_start(box, True, True, 0)

    def _init_colour_controls(self):
        # build controls
        self._r_ctrl = ScaleEntry('R', 0, 255, 1, 1, 0.1, 0.3)
        self._g_ctrl = ScaleEntry('G', 0, 255, 1, 0, 0.5, 0)
        self._b_ctrl = ScaleEntry('B', 0, 255, 1, 0, 0.5, 1)
        self._h_ctrl = ScaleEntry('H', 0, 359, 1, wrap=True)
        self._s_ctrl = ScaleEntry('S', 0, 100, 1)
        self._v_ctrl = ScaleEntry('V', 0, 100, 1)

        # alignments for padding
        a1 = Gtk.Alignment()
        a1.set_padding(config.MAIN_GUTTER_PX, 0, 0, 0)
        a1.add(self._r_ctrl)
        a2 = Gtk.Alignment()
        a2.set_padding(config.MAIN_GUTTER_PX, 0, 0, 0)
        a2.add(self._h_ctrl)

        # register listeners
        self._r_ctrl.on_change(self._update_model_from_rgb)
        self._g_ctrl.on_change(self._update_model_from_rgb)
        self._b_ctrl.on_change(self._update_model_from_rgb)
        self._h_ctrl.on_change(self._update_model_from_hsv)
        self._s_ctrl.on_change(self._update_model_from_hsv)
        self._v_ctrl.on_change(self._update_model_from_hsv)

        self._main_box.pack_start(a1, True, True, 0)
        self._main_box.pack_start(self._g_ctrl, True, True, 0)
        self._main_box.pack_start(self._b_ctrl, True, True, 0)
        self._main_box.pack_start(a2, True, True, 0)
        self._main_box.pack_start(self._s_ctrl, True, True, 0)
        self._main_box.pack_start(self._v_ctrl, True, True, 0)

    @staticmethod
    def _new_css_entry_hbox(label, entry):
        # label
        lbl = Gtk.Label()
        lbl.modify_font(Pango.FontDescription('sans-serif bold 8'))
        lbl.set_text(label)
        lbl.set_alignment(0, 0)
        color = Gdk.Color(red=config.TEXT_COLOUR_R * 65535,
                          green=config.TEXT_COLOUR_G * 65535,
                          blue=config.TEXT_COLOUR_B * 65535)
        lbl.modify_fg(Gtk.StateType.NORMAL, color)

        # box
        hbox = Gtk.HBox(spacing=config.MAIN_GUTTER_PX, homogeneous=False)
        hbox.pack_start(lbl, False, False, 0)
        hbox.pack_start(entry, False, False, 0)

        return hbox

    @staticmethod
    def _new_bool_option_alignment(label):
        # option
        opt = Gtk.CheckButton(label=label)
        opt.modify_font(Pango.FontDescription('sans-serif 8'))
        color = Gdk.Color(red=config.TEXT_COLOUR_R * 65535,
                          green=config.TEXT_COLOUR_G * 65535,
                          blue=config.TEXT_COLOUR_B * 65535)
        opt.modify_fg(Gtk.StateType.NORMAL, color)

        # aligment for extra padding
        opt_a = Gtk.Alignment()
        opt_a.set_padding(0, 0, config.MAIN_GUTTER_PX, 0)
        opt_a.add(opt)

        return opt, opt_a

    def _init_css_entries(self):
        # hex entry
        self._css_hex_entry = HexEntry()
        self._css_hex_entry.on_change(self._update_model_from_css_hex)

        # RGB entry
        self._css_rgb_entry = RgbEntry()
        self._css_rgb_entry.on_change(self._update_model_from_css_rgb)

        # hboxes
        css_hex_hbox = MainWindow._new_css_entry_hbox('Hex: ', self._css_hex_entry)
        css_rgb_hbox = MainWindow._new_css_entry_hbox('RGB: ', self._css_rgb_entry)

        # add options to hex box
        self._css_hex_copy_hash_opt, a1 = MainWindow._new_bool_option_alignment('Copy #')
        self._css_hex_copy_hash_opt_toggled_handler = self._css_hex_copy_hash_opt.connect('toggled', self._on_css_hex_copy_hash_toggled)
        self._css_hex_lower_opt, a2 = MainWindow._new_bool_option_alignment('Lowercase')
        self._css_hex_lower_opt_toggled_handler = self._css_hex_lower_opt.connect('toggled', self._on_css_hex_lower_toggled)
        css_hex_hbox.pack_start(a1, False, False, 0)
        css_hex_hbox.pack_start(a2, False, False, 0)

        # alignment for hex box
        css_hex_a = Gtk.Alignment()
        css_hex_a.set_padding(config.MAIN_GUTTER_PX, 0, 0, 0)
        css_hex_a.add(css_hex_hbox)

        self._main_box.pack_start(css_hex_a, True, True, 0)
        self._main_box.pack_start(css_rgb_hbox, True, True, 0)

    def _init_all(self):
        # big colour
        self._init_big_colour()

        # fine colour controls
        self._init_fine_colour_controls()

        # colour controls
        self._init_colour_controls()

        # hex
        self._init_css_entries()

    def _on_css_hex_copy_hash_toggled(self, btn):
        self._update_model_from_settings()

    def _on_css_hex_lower_toggled(self, btn):
        self._update_model_from_settings()

    def _on_inc_light_clicked(self, btn):
        self._model.colour.inc_light(self._model.fine_incr)
        self._update_view('fine')

    def _on_dec_light_clicked(self, btn):
        self._model.colour.dec_light(self._model.fine_incr)
        self._update_view('fine')

    def _on_inc_sat_clicked(self, btn):
        self._model.colour.inc_sat(self._model.fine_incr)
        self._update_view('fine')

    def _on_dec_sat_clicked(self, btn):
        self._model.colour.dec_sat(self._model.fine_incr)
        self._update_view('fine')

    def _get_rgb_ctrl_values(self):
        r = self._r_ctrl.get_value()
        g = self._g_ctrl.get_value()
        b = self._b_ctrl.get_value()

        return r, g, b

    def _get_hsv_ctrl_values(self):
        h = self._h_ctrl.get_value()
        s = self._s_ctrl.get_value()
        v = self._v_ctrl.get_value()

        return h, s, v

    def _enable_hsv_events(self, en):
        self._h_ctrl.enable_on_change(en)
        self._s_ctrl.enable_on_change(en)
        self._v_ctrl.enable_on_change(en)

    def _update_model_from_rgb(self):
        r, g, b = self._get_rgb_ctrl_values()
        self._model.colour.set_rgb(r, g, b)
        self._update_view('rgb')

    def _update_model_from_hsv(self):
        h, s, v = self._get_hsv_ctrl_values()
        s /= 100
        v /= 100
        self._model.colour.set_hsv(h, s, v)
        self._update_view('hsv')

    def _update_model_from_css_hex(self):
        colour = self._css_hex_entry.get_colour()
        self._model.colour = colour
        self._update_view('css-hex')

    def _update_model_from_css_rgb(self):
        colour = self._css_rgb_entry.get_colour()
        self._model.colour = colour
        self._update_view('css-rgb')

    def _update_model_from_settings(self):
        self._model.css_hex_copy_hash = self._css_hex_copy_hash_opt.get_active()
        self._model.css_hex_lower = self._css_hex_lower_opt.get_active()
        self._update_settings()

    def _update_big_colour(self):
        self._big_colour.set_colour(self._model.colour)

    def _update_rgb_ctrls(self):
        r, g, b = self._model.colour.get_rgb()
        self._r_ctrl.set_value_no_emit(r)
        self._g_ctrl.set_value_no_emit(g)
        self._b_ctrl.set_value_no_emit(b)

    def _update_hsv_ctrls(self):
        h, s, v = self._model.colour.get_hsv()
        self._h_ctrl.set_value_no_emit(h)
        self._s_ctrl.set_value_no_emit(s * 100)
        self._v_ctrl.set_value_no_emit(v * 100)

    def _update_css_hex(self):
        self._css_hex_entry.set_colour_no_emit(self._model.colour)

    def _update_css_rgb(self):
        self._css_rgb_entry.set_colour_no_emit(self._model.colour)

    def _update_settings(self):
        self._css_hex_copy_hash_opt.handler_block(self._css_hex_copy_hash_opt_toggled_handler)
        self._css_hex_lower_opt.handler_block(self._css_hex_lower_opt_toggled_handler)

        self._css_hex_copy_hash_opt.set_active(self._model.css_hex_copy_hash)
        self._css_hex_lower_opt.set_active(self._model.css_hex_lower)

        self._css_hex_copy_hash_opt.handler_unblock(self._css_hex_copy_hash_opt_toggled_handler)
        self._css_hex_lower_opt.handler_unblock(self._css_hex_lower_opt_toggled_handler)

        self._css_hex_entry.set_copy_hash(self._model.css_hex_copy_hash)
        self._css_hex_entry.set_lower(self._model.css_hex_lower)

    def _update_view(self, focused_ctrl):
        self._update_big_colour()
        if focused_ctrl != 'hsv':
            self._update_hsv_ctrls()
        if focused_ctrl != 'rgb':
            self._update_rgb_ctrls()
        if focused_ctrl != 'css-hex':
            self._update_css_hex()
        if focused_ctrl != 'css-rgb':
            self._update_css_rgb()
        self._update_settings()
