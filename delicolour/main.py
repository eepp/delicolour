import gi


# required GI versions/features
gi.require_version('Gtk', '3.0')


from delicolour import main_window
from gi.repository import Gtk
import delicolour
import argparse
import warnings
import signal


def _parse_args():
    ap = argparse.ArgumentParser()

    ap.add_argument('-i', '--init', action='store', metavar='HEX',
                    help='initial color (CSS hex)')
    ap.add_argument('-V', '--version', action='version',
                    version='%(prog)s v{}'.format(delicolour.__version__))

    # parse args
    args = ap.parse_args()

    return args


def run():
    # enable SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # see <https://bugzilla.gnome.org/show_bug.cgi?id=708676#c4>
    warnings.filterwarnings('ignore', '.*g_value_get_int.*', Warning)

    # main app
    args = _parse_args()
    win = main_window.MainWindow(args)
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()
