import math
from gi.repository import Gtk, Gdk
from delicolour.colour import Colour


class FavColour(Gtk.DrawingArea):
    def __init__(self, width, height):
        # initialize drawing area
        super().__init__()
        self.set_size_request(width, height)
        self.connect('draw', self._on_draw)

        # initialize click action
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.connect('button-press-event', self._on_click)

        # user events
        self._user_on_click = None

        # set initial color
        self.set_colour(Colour.from_rgb(255, 255, 255))

    def _get_size(self):
        alloc = self.get_allocation()

        return alloc.width, alloc.height

    def _notify_on_click(self, event):
        if self._user_on_click:
            self._user_on_click(event, self)

    def _on_click(self, widget, event):
        self._notify_on_click(event)

    def _on_draw(self, drawing_area, cr):
        def do_path():
            cr.rectangle(lw, lw, width - 2 * lw, height - 2 * lw)

        def set_source_rgb(colour):
            r, g, b = colour.rgb
            r /= 255
            g /= 255
            b /= 255
            cr.set_source_rgb(r, g, b)

        width, height = self._get_size()
        lw = 2

        # fill colour 1
        set_source_rgb(self._colour)
        do_path()
        cr.fill()

        # stroke around everything
        cr.set_line_width(lw)
        cr.set_source_rgb(.3, .3, .3)
        do_path()
        cr.stroke()

        return False

    def set_colour(self, colour):
        self._colour = colour
        self.set_tooltip_text('#' + self._colour.hex)
        self.queue_draw()

    @property
    def colour(self):
        return self._colour

    def on_click(self, cb):
        self._user_on_click = cb
