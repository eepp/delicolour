import math
from delicolour.colour import Colour
from gi.repository import Gtk


class BigColour(Gtk.DrawingArea):
    def __init__(self, border_radius=8):
        # initial colour is black
        self._colour = Colour.from_rgb(0, 0, 0)

        # save border radius
        self._border_radius = border_radius

        # initialize drawing area
        Gtk.DrawingArea.__init__(self)
        self.set_size_request(350, 75)
        self.connect('draw', self._on_draw)

    def _get_size(self):
        alloc = self.get_allocation()

        return alloc.width, alloc.height

    def _on_draw(self, drawing_area, cr):
        width, height = self._get_size()
        br = self._border_radius

        # set colour
        r, g, b = self._colour.get_rgb()
        cr.set_source_rgb(r, g, b)

        # actual shape
        cr.set_line_width(0)
        cr.move_to(br, 0)
        cr.arc(width - br, br, br, -0.5 * math.pi, 0)
        cr.arc(width - br, height - br, br, 0, 0.5 * math.pi)
        cr.arc(br, height - br, br, 0.5 * math.pi, 1 * math.pi)
        cr.arc(br, br, br, 1 * math.pi, -0.5 * math.pi)
        cr.close_path()

        # fill now
        cr.fill()

        return False

    def set_colour(self, colour):
        self._colour = colour
        self.queue_draw()

    def set_rgb(self, r, g, b):
        self._colour.set_rgb(r, g, b)
        self.queue_draw()

