from delicolour import config
from delicolour.scale_entry import ScaleEntry
from delicolour.big_colour import BigColour
from gi.repository import Gtk


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="delicolour")
        self._make_me_nice()
        self._init_main_box()

    def _make_me_nice(self):
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(config.MAIN_GUTTER_PX)
        self.set_resizable(False)

    def _init_main_box(self):
        self._main_box = Gtk.VBox(spacing=config.MAIN_GUTTER_PX,
                                  homogeneous=False)
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
        self._r_ctrl = ScaleEntry('R', 0, 255, 1, 1, 0.1, 0.3)
        self._g_ctrl = ScaleEntry('G', 0, 255, 1, 0, 0.5, 0)
        self._b_ctrl = ScaleEntry('B', 0, 255, 1, 0, 0.5, 1)
        self._h_ctrl = ScaleEntry('H', 0, 100, 1)
        self._s_ctrl = ScaleEntry('S', 0, 100, 1)
        self._v_ctrl = ScaleEntry('V', 0, 100, 1)
        a = Gtk.Alignment()
        a.set_padding(config.MAIN_GUTTER_PX, 0, 0, 0)
        a.add(self._h_ctrl)


        self._colour_box.pack_start(self._r_ctrl, True, True, 0)
        self._colour_box.pack_start(self._g_ctrl, True, True, 0)
        self._colour_box.pack_start(self._b_ctrl, True, True, 0)
        self._colour_box.pack_start(a, True, True, 0)
        self._colour_box.pack_start(self._s_ctrl, True, True, 0)
        self._colour_box.pack_start(self._v_ctrl, True, True, 0)

    def _init_colour_frame(self):
        # big colour
        self._init_big_colour()

        # fine colour controls
        self._init_fine_colour_controls()

        # colour controls
        self._init_colour_controls()




