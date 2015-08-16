import gi


# required GI versions/features
gi.require_version('Gtk', '3.0')


from delicolour import main_window
from delicolour import config
from gi.repository import Gtk
import delicolour
import argparse
import warnings
import signal
import sys


def _perror(msg):
    print('Error: ' + str(msg), file=sys.stderr)
    sys.exit(1)


def _parse_args():
    ap = argparse.ArgumentParser()

    ap.add_argument('-f', '--fav-colours-count', action='store', type=int,
                    metavar='COUNT', default=12,
                    help='number of fav colours per row (default: 12)')
    ap.add_argument('-F', '--fav-colours-rows-count', action='store', type=int,
                    metavar='COUNT', default=1,
                    help='number of rows of fav colours (default: 1)')
    ap.add_argument('-i', '--increment', action='store', metavar='VALUE',
                    type=int, default=1,
                    help='fine-tuning increment (default: 1)')
    ap.add_argument('-l', '--left-colour', action='store', metavar='HEX',
                    help='initial left color (CSS hex)')
    ap.add_argument('-r', '--right-colour', action='store', metavar='HEX',
                    help='initial right color (CSS hex)')
    ap.add_argument('-V', '--version', action='version',
                    version='%(prog)s v{}'.format(delicolour.__version__))

    # parse args
    args = ap.parse_args()

    # validate --fav-colours-count
    if args.fav_colours_count < 1 or args.fav_colours_count > 16:
        _perror('--fav-colours-count must be in [1, 16] range')

    # validate --fav-colours-rows-count
    if args.fav_colours_rows_count < 1 or args.fav_colours_rows_count > 4:
        _perror('--fav-colours-rows-count must be in [1, 4] range')

    # validate --increment
    mn = config.INCR_SPINNER_MIN_VAL
    mx =  config.INCR_SPINNER_MAX_VAL

    if args.increment < mn or args.increment > mx:
        _perror('--increment must be in [{}, {}] range'.format(mn, mx))

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
