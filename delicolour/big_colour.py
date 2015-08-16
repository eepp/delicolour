import math
from gi.repository import Gtk, Gdk
from delicolour.colour import Colour


class BigColour(Gtk.DrawingArea):
    def __init__(self, border_radius=4, height=75):
        # initial colours
        self._colour1 = Colour.from_rgb(0, 0, 0)
        self._colour2 = Colour.from_rgb(0, 0, 0)
        self._sel = 1

        # save border radius
        self._border_radius = border_radius

        # initialize drawing area
        super().__init__()
        self.set_size_request(0, height)
        self.connect('draw', self._on_draw)

        # initialize click action
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.connect('button-press-event', self._on_click)

        # user events
        self._user_on_sel_change = None

    def _get_size(self):
        alloc = self.get_allocation()

        return alloc.width, alloc.height

    def _notify_on_sel_change(self, sel):
        if self._user_on_sel_change:
            self._user_on_sel_change(sel)

    def _on_click(self, widget, event):
        x = int(event.x)
        width, height = self._get_size()

        if x < round(width / 2):
            self._set_sel(1)
        else:
            self._set_sel(2)

        self._notify_on_sel_change(self._sel)

    def _on_draw(self, drawing_area, cr):
        def do_rect_path():
            # rectangle with rounded corners
            cr.arc(width - br - lw, br + lw, br, -0.5 * math.pi, 0)
            cr.arc(width - br - lw, height - br - lw, br, 0, 0.5 * math.pi)
            cr.arc(br + lw, height - br - lw, br, 0.5 * math.pi, 1 * math.pi)
            cr.arc(br + lw, br + lw, br, 1 * math.pi, -0.5 * math.pi)
            cr.close_path()

        def do_half_path():
            cr.arc(width - br - lw, br + lw, br, -0.5 * math.pi, 0)
            cr.arc(width - br - lw, height - br - lw, br, 0, 0.5 * math.pi)
            cr.line_to(round(width / lw) - diag_dist, height - lw)
            cr.line_to(round(width / lw) + diag_dist, lw)
            cr.close_path()

        def set_source_rgb(colour):
            r, g, b = colour.rgb
            r /= 255
            g /= 255
            b /= 255
            cr.set_source_rgb(r, g, b)

        def do_dot_path(x, y):
            cr.save()
            cr.translate(x, y)
            cr.scale(dot_rad, dot_rad);
            cr.arc(0, 0, 1, 0, 2 * math.pi)
            cr.set_source_rgb(0, 0, 0)
            cr.restore()

        def draw_sel_dot():
            tr_y = dot_dist

            if self._sel == 1:
                tr_x = dot_dist + lw
            else:
                tr_x = width - dot_dist - lw

            do_dot_path(tr_x, tr_y)
            cr.fill()
            do_dot_path(tr_x, tr_y)
            cr.set_line_width(1)
            cr.set_source_rgb(1, 1, 1)
            cr.stroke()

        width, height = self._get_size()
        br = self._border_radius
        lw = 2
        dot_rad = 3
        dot_dist = 10
        diag_dist = 5

        # fill colour 1
        set_source_rgb(self._colour1)
        do_rect_path()
        cr.fill()

        # fill colour 2
        set_source_rgb(self._colour2)
        do_half_path()
        cr.fill()

        # stroke around everything
        cr.set_line_width(lw)
        cr.set_source_rgb(0.3, 0.3, 0.3)
        do_rect_path()
        cr.stroke()

        # draw selrent dot
        draw_sel_dot()

        return False

    def set_colour1(self, colour):
        self._colour1 = colour
        self.queue_draw()

    def set_colour2(self, colour):
        self._colour2 = colour
        self.queue_draw()

    def set_rgb1(self, r, g, b):
        self._colour1.set_rgb(r, g, b)
        self.queue_draw()

    def set_rgb2(self, r, g, b):
        self._colour2.set_rgb(r, g, b)
        self.queue_draw()

    def set_sel(self, sel):
        self._set_sel(sel)

    def _set_sel(self, sel):
        self._sel = sel
        self.queue_draw()

    def on_sel_change(self, cb):
        self._user_on_sel_change = cb
