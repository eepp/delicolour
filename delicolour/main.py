from delicolour import main_window
from gi.repository import Gtk
import signal

def main():
    # enable Ctrl+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # main app
    win = main_window.MainWindow()
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()
