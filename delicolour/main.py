from delicolour import main_window
from gi.repository import Gtk


def main():
    win = main_window.MainWindow()
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()
