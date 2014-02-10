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
        def do_path():
            cr.move_to(br + 2, 2)
            cr.arc(width - br - 2, br + 2, br, -0.5 * math.pi, 0)
            cr.arc(width - br - 2, height - br - 2, br, 0, 0.5 * math.pi)
            cr.arc(br + 2, height - br - 2, br, 0.5 * math.pi, 1 * math.pi)
            cr.arc(br + 2, br + 2, br, 1 * math.pi, -0.5 * math.pi)
            cr.close_path()

        width, height = self._get_size()
        br = self._border_radius

        # set colour
        r, g, b = self._colour.get_rgb()
        r /= 255
        g /= 255
        b /= 255
        cr.set_source_rgb(r, g, b)

        # fill
        do_path()
        cr.fill()

        # stroke
        cr.set_line_width(2)
        cr.set_source_rgb(0.3, 0.3, 0.3)
        do_path()
        cr.stroke()

        return False

    def set_colour(self, colour):
        self._colour = colour
        self.queue_draw()

    def set_rgb(self, r, g, b):
        self._colour.set_rgb(r, g, b)
        self.queue_draw()

