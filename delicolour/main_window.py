from delicolour.fine_controls import FineControls
from delicolour.css_hex_entry import CssHexEntry
from delicolour.css_rgb_entry import CssRgbEntry
from delicolour.fav_colours import FavColours
from delicolour.scale_entry import ScaleEntry
from delicolour.big_colour import BigColour
from delicolour.app_model import AppModel
from delicolour.colour import Colour
from gi.repository import Pango
from delicolour import config
from gi.repository import Gtk
from gi.repository import Gdk
from functools import partial


class MainWindow(Gtk.Window):
    def __init__(self, args):
        super().__init__(title='delicolour')
        self._args = args
        self._make_me_nice()
        self._init_main_box()
        self._init_keyb()
        self._model = AppModel.get_default()
        self._apply_args()
        self._update_view('init')

    def _apply_arg_init(self, init):
        try:
            colour = Colour.from_hex(init)
        except:
            return

        self._model.colour = colour

    def _apply_args(self):
        if self._args.left_colour is not None:
            try:
                colour = Colour.from_hex(self._args.left_colour)
                self._model.colour1 = colour
            except:
                pass

        if self._args.right_colour is not None:
            try:
                colour = Colour.from_hex(self._args.right_colour)
                self._model.colour2 = colour
            except:
                pass

        self._model.fine_incr = self._args.increment

    def _make_me_nice(self):
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(round(config.MAIN_GUTTER_PX * 1.5))
        self.set_resizable(False)

    def _init_keyb(self):
        self.connect('key_press_event', self._on_key_press)

    def _on_key_press(self, widget, event):
        key_name = Gdk.keyval_name(event.keyval)

        if key_name == 'z':
            # set to black
            self._set_model_rgb(0, 0, 0)
        elif key_name == 'x':
            # set to white
            self._set_model_rgb(255, 255, 255)
        elif key_name == 'minus' or key_name == 'KP_Subtract':
            # decrease lightness
            self._on_dec_light()
        elif key_name == 'plus' or key_name == 'equal' or key_name == 'KP_Add':
            # increase lightness
            self._on_inc_light()
        elif key_name == 'q':
            # decrease saturation
            self._on_dec_sat()
        elif key_name == 'w':
            # increase saturation
            self._on_inc_sat()
        elif key_name == 'numbersign':
            # swap colours
            if self._model.sel == 1:
                self._model.sel = 2
            else:
                self._model.sel = 1

            self._update_view()

    def _init_main_box(self):
        self._main_box = Gtk.Box(spacing=config.MAIN_GUTTER_PX,
                                 homogeneous=False)
        self._main_box.set_orientation(Gtk.Orientation.VERTICAL)
        self._main_box.set_size_request(320, 0)
        self.add(self._main_box)
        self._init_all()

    def _init_big_colour(self):
        self._big_colour = BigColour()
        self._big_colour.on_sel_change(self._on_sel_change)
        self._main_box.pack_start(self._big_colour, True, True, 0)

    def _init_fav_colours(self):
        fav_colours_count = self._args.fav_colours_count

        for i in range(self._args.fav_colours_rows_count):
            self._fav_colours = FavColours(fav_colours_count=fav_colours_count)
            self._fav_colours.on_fav_colour_click(self._on_fav_colour_click)
            self._main_box.pack_start(self._fav_colours, True, True, 0)

    def _init_fine_colour_controls(self):
        # fine controls
        self._fine_controls = FineControls(config.INCR_SPINNER_MIN_VAL,
                                           config.INCR_SPINNER_MAX_VAL,
                                           self._args.increment)
        self._main_box.pack_start(self._fine_controls, True, True, 0)

        # set callbacks
        self._fine_controls.on_inc_light(self._on_inc_light)
        self._fine_controls.on_dec_light(self._on_dec_light)
        self._fine_controls.on_inc_sat(self._on_inc_sat)
        self._fine_controls.on_dec_sat(self._on_dec_sat)
        self._fine_controls.on_incr_change(self._update_model_from_incr)

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
        self._r_ctrl.on_key_press(partial(self._on_scale_entry_key_press, 'r'))
        self._g_ctrl.on_key_press(partial(self._on_scale_entry_key_press, 'g'))
        self._b_ctrl.on_key_press(partial(self._on_scale_entry_key_press, 'b'))

        # pack
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
        lbl.modify_font(Pango.FontDescription('sans-serif 8'))
        lbl.set_text(label)
        lbl.set_width_chars(4)
        lbl.set_alignment(0, 0.5)
        color = Gdk.Color(red=config.TEXT_COLOUR_R * 65535,
                          green=config.TEXT_COLOUR_G * 65535,
                          blue=config.TEXT_COLOUR_B * 65535)
        lbl.modify_fg(Gtk.StateType.NORMAL, color)

        # box
        hbox = Gtk.Box(spacing=config.MAIN_GUTTER_PX, homogeneous=False)
        hbox.props.valign = Gtk.Align.CENTER
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
        self._css_hex_entry = CssHexEntry()
        self._css_hex_entry.on_change(self._update_model_from_css_hex)

        # RGB entry
        self._css_rgb_entry = CssRgbEntry()
        self._css_rgb_entry.on_change(self._update_model_from_css_rgb)

        # hboxes
        css_hex_hbox = MainWindow._new_css_entry_hbox('Hex:', self._css_hex_entry)
        css_rgb_hbox = MainWindow._new_css_entry_hbox('RGB:', self._css_rgb_entry)

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
        # fav colours
        self._init_fav_colours()

        # big colour
        self._init_big_colour()

        # fine colour controls
        self._init_fine_colour_controls()

        # colour controls
        self._init_colour_controls()

        # hex
        self._init_css_entries()

    def _on_fav_colour_click(self, event, fav_colour):
        if event.button == 1:
            self._model.colour = fav_colour.colour
            self._update_view()
        elif event.button == 3:
            fav_colour.set_colour(self._model.colour.copy())
            self._update_view()

    def _on_sel_change(self, sel):
        self._model.sel = sel
        self._update_view()

    def _on_css_hex_copy_hash_toggled(self, btn):
        self._update_model_from_settings()
        self._update_view()

    def _on_css_hex_lower_toggled(self, btn):
        self._update_model_from_settings()
        self._update_view()

    def _on_inc_light(self):
        self._model.colour.inc_light(self._model.fine_incr / 100)
        self._update_view()

    def _on_dec_light(self):
        self._model.colour.dec_light(self._model.fine_incr / 100)
        self._update_view()

    def _on_inc_sat(self):
        self._model.colour.inc_sat(self._model.fine_incr / 100)
        self._update_view()

    def _on_dec_sat(self):
        self._model.colour.dec_sat(self._model.fine_incr / 100)
        self._update_view()

    def _on_scale_entry_key_press(self, origin, key_name):
        if origin == key_name:
            return

        r, g, b = self._model.colour.rgb

        if origin == 'r':
            origin_value = self._r_ctrl.value
        elif origin == 'g':
            origin_value = self._g_ctrl.value
        elif origin == 'b':
            origin_value = self._b_ctrl.value

        if key_name == 'r':
            r = origin_value
        elif key_name == 'g':
            g = origin_value
        elif key_name == 'b':
            b = origin_value

        self._set_model_rgb(r, g, b)

    def _update_model_from_incr(self):
        incr = self._fine_controls.incr_value
        self._model.fine_incr = incr
        self._update_all_incr()

    def _get_rgb_ctrl_values(self):
        r = self._r_ctrl.value
        g = self._g_ctrl.value
        b = self._b_ctrl.value

        return r, g, b

    def _get_hsv_ctrl_values(self):
        h = self._h_ctrl.value
        s = self._s_ctrl.value
        v = self._v_ctrl.value

        return h, s, v

    def _enable_hsv_events(self, en):
        self._h_ctrl.enable_on_change(en)
        self._s_ctrl.enable_on_change(en)
        self._v_ctrl.enable_on_change(en)

    def _set_model_rgb(self, r, g, b):
        self._model.colour.set_rgb(r, g, b)
        self._update_view()

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
        colour = self._css_hex_entry.colour
        self._model.colour = colour
        self._update_view('css-hex')

    def _update_model_from_css_rgb(self):
        colour = self._css_rgb_entry.colour
        self._model.colour = colour
        self._update_view('css-rgb')

    def _update_model_from_settings(self):
        self._model.css_hex_copy_hash = self._css_hex_copy_hash_opt.get_active()
        self._model.css_hex_lower = self._css_hex_lower_opt.get_active()
        self._update_settings()

    def _update_big_colour(self):
        self._big_colour.set_colour1(self._model.colour1)
        self._big_colour.set_colour2(self._model.colour2)
        self._big_colour.set_sel(self._model.sel)

    def _update_rgb_ctrls(self):
        r, g, b = self._model.colour.rgb
        self._r_ctrl.set_value_no_emit(r)
        self._g_ctrl.set_value_no_emit(g)
        self._b_ctrl.set_value_no_emit(b)

    def _update_hsv_ctrls(self):
        h, s, v = self._model.colour.hsv
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

    def _update_all_incr(self):
        self._r_ctrl.set_page_incr(self._model.fine_incr)
        self._g_ctrl.set_page_incr(self._model.fine_incr)
        self._b_ctrl.set_page_incr(self._model.fine_incr)
        self._h_ctrl.set_page_incr(self._model.fine_incr)
        self._s_ctrl.set_page_incr(self._model.fine_incr)
        self._v_ctrl.set_page_incr(self._model.fine_incr)

    def _update_title(self):
        def get_color_title(colour, sel_colour):
            if colour is sel_colour:
                fmt = '[#{}]'
            else:
                fmt = '#{}'

            hx = colour.hex

            if not self._model.css_hex_lower:
                hx = hx.upper()

            return fmt.format(hx)

        fmt = 'delicolour: {} {}'
        colour1_title = get_color_title(self._model.colour1, self._model.colour)
        colour2_title = get_color_title(self._model.colour2, self._model.colour)
        title = fmt.format(colour1_title, colour2_title)
        self.set_title(title)

    def _update_view(self, focused_ctrl=None):
        self._update_title()
        self._update_big_colour()

        if focused_ctrl != 'hsv':
            self._update_hsv_ctrls()

        if focused_ctrl != 'rgb':
            self._update_rgb_ctrls()

        if focused_ctrl != 'css-hex':
            self._update_css_hex()

        if focused_ctrl != 'css-rgb':
            self._update_css_rgb()

        if focused_ctrl == 'init':
            self._update_settings()
            self._update_all_incr()
