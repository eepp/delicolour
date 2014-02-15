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
        self._main_box.set_size_request(350, 0)
        self.add(self._main_box)
        self._init_frames()

    @staticmethod
    def _new_frame_box(label):
        frame = Gtk.Frame(label=label)
        frame.set_shadow_type(Gtk.ShadowType.IN)
        vbox = Gtk.VBox(spacing=config.MAIN_GUTTER_PX, homogeneous=False)
        vbox.set_border_width(config.MAIN_GUTTER_PX)
        frame.add(vbox);

        return frame, vbox

    def _init_frames(self):
        # create frames
        colour_frame, self._colour_box = MainWindow._new_frame_box('Colour')
        settings_frame, self._settings_box = MainWindow._new_frame_box('Settings')

        # pack them into the main box
        self._main_box.pack_start(colour_frame, True, True, 0)
        self._main_box.pack_start(settings_frame, True, True, 0)

        # initialize them
        self._init_colour_frame()

    def _init_big_colour(self):
        self._big_colour = BigColour()
        self._colour_box.pack_start(self._big_colour, True, True, 0)

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
        self._colour_box.pack_start(box, True, True, 0)

    def _init_colour_controls(self):
        # build controls
        self._r_ctrl = ScaleEntry('R', 0, 255, 1, 1, 0.1, 0.3)
        self._g_ctrl = ScaleEntry('G', 0, 255, 1, 0, 0.5, 0)
        self._b_ctrl = ScaleEntry('B', 0, 255, 1, 0, 0.5, 1)
        self._h_ctrl = ScaleEntry('H', 0, 359, 1, wrap=True)
        self._s_ctrl = ScaleEntry('S', 0, 100, 1)
        self._v_ctrl = ScaleEntry('V', 0, 100, 1)
        a = Gtk.Alignment()
        a.set_padding(config.MAIN_GUTTER_PX, 0, 0, 0)
        a.add(self._h_ctrl)

        # register listeners
        self._r_ctrl.on_change(self._update_model_from_rgb)
        self._g_ctrl.on_change(self._update_model_from_rgb)
        self._b_ctrl.on_change(self._update_model_from_rgb)
        self._h_ctrl.on_change(self._update_model_from_hsv)
        self._s_ctrl.on_change(self._update_model_from_hsv)
        self._v_ctrl.on_change(self._update_model_from_hsv)

        self._colour_box.pack_start(self._r_ctrl, True, True, 0)
        self._colour_box.pack_start(self._g_ctrl, True, True, 0)
        self._colour_box.pack_start(self._b_ctrl, True, True, 0)
        self._colour_box.pack_start(a, True, True, 0)
        self._colour_box.pack_start(self._s_ctrl, True, True, 0)
        self._colour_box.pack_start(self._v_ctrl, True, True, 0)

    @staticmethod
    def _new_css_hbox(label, entry):
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

    def _init_css(self):
        # hex entry
        self._css_hex_entry = HexEntry()
        self._css_hex_entry.on_change(self._update_model_from_css_hex)

        # RGB entry
        self._css_rgb_entry = RgbEntry()
        self._css_rgb_entry.on_change(self._update_model_from_css_rgb)

        # hboxes
        css_hex_hbox = MainWindow._new_css_hbox('Hex: ', self._css_hex_entry)
        css_rgb_hbox = MainWindow._new_css_hbox('RGB: ', self._css_rgb_entry)

        # alignment for hex box
        css_hex_a = Gtk.Alignment()
        css_hex_a.set_padding(config.MAIN_GUTTER_PX, 0, 0, 0)
        css_hex_a.add(css_hex_hbox)

        self._colour_box.pack_start(css_hex_a, True, True, 0)
        self._colour_box.pack_start(css_rgb_hbox, True, True, 0)

    def _init_colour_frame(self):
        # big colour
        self._init_big_colour()

        # fine colour controls
        self._init_fine_colour_controls()

        # colour controls
        self._init_colour_controls()

        # hex
        self._init_css()

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
