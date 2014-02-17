delicolour
==========

**delicolour** is a lightweight colour finder. It's written in Python using
PyGObject (i.e. GTK). It has only been tested on Linux.

![delicolour screenshot](http://0x3b.org/ss/oopack386.png)

(I don't have any GTK theme so it could look better with your setup).

My goal here is to have a straightforward interface for choosing a colour
(mainly for Web design), not as advanced as
[Gpick](https://code.google.com/p/gpick/), but still useful and very fluid.
The main core principle is: no tabs or other windows, everything accessible
from the main window.

This project is also a pretext for trying PyGObject.


features
--------

* instant updates (move one slider and everything else is set live)
* big colour rectangle showing your current choice
* RGB values (0 to 255)
* HSV values (0 to 359 for hue and 0 to 100 for saturation and value)
* scrollable sliders and entries (hue wraps)
* fine colour adjustment buttons (increase/decrease saturation/lightness)
  with adjustable increment value
* hex and RGB CSS strings
* intelligent copy/paste (paste `#rrggbb` or `rrggbb` into the hex entry
  and decide if you want to prepend the `#` sign when copying)
* pressing Ctrl+C without having anything selected in the entry box will
  copy everything anyway (same thing when pasting)


deps
----

You need:

* Python 3 with:
    * PyGObject
    * NumPy
    * [Color Math](https://github.com/gtaylor/python-colormath)
      (use `pip install colormath` for this)

I'm pretty sure you can find this easily for your distribution.


using
-----

Do:

    git clone https://github.com/eepp/delicolour
    cd delicolour
    PYTHONPATH=$(pwd) bin/delicolour-ui.py

If this doesn't work because Python 2 is still the default Python
interpreter for your distribution, use Python 3 directly:

    PYTHONPATH=$(pwd) python3 bin/delicolour-ui.py


todo
----

* colour picker for whole display
* secondary colour
