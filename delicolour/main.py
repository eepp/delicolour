from delicolour import main_window
from gi.repository import Gtk
import signal
import warnings


def run():
    # enable SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # see <https://bugzilla.gnome.org/show_bug.cgi?id=708676#c4>
    warnings.filterwarnings('ignore', '.*g_value_get_int.*', Warning)

    # main app
    win = main_window.MainWindow()
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()
