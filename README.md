# delicolour

**_delicolour_** is a lightweight _colour finder_. It uses Gtk+ 3.
It has only been tested on Linux.

![delicolour screenshot](http://ss.0x3b.org/refixing219.png)

The goal of delicolour is to have a straightforward interface for
choosing a colour (mainly for Web design), not as advanced as
[Gpick](http://www.gpick.org/), yet still useful and very fluid. The
core principle is: no tabs or other windows, everything accessible
from the main window.


## Notable features

  * Instant updates (moving one slider or modifying one field updates
    the other controls)
  * Big colour rectangle showing your two current colours
  * Up to four rows of 16 favorite colours at the top (number of rows
    and colours per rows is configurable with command-line options)
  * RGB values (0 to 255)
  * HSV values (0 to 359 for hue and 0 to 100 for saturation and value)
  * Scrollable sliders and entries (hue wraps)
  * Fine colour adjustment buttons (increase/decrease saturation and
    lightness) with adjustable increment value
  * CSS hex and RGB strings
  * Intelligent copy/paste (paste `#rrggbb` or `rrggbb` into the hex
    text box and decide if you want to prepend the `#` character when
    copying)
  * Useful keyboard shortcuts


## Installing

In order to install delicolour, the following packages must be installed
on your system:

  * Python 3
  * [PyGObject](https://wiki.gnome.org/action/show/Projects/PyGObject) 3
  * GTK+ 3
  * pip for Python 3

The following instructions show how to do so on a few major
distributions:

**Ubuntu**:

    sudo apt-get install python3-pip python3-gi python3-gi-cairo
    sudo pip3 install delicolour

**Debian**:

    sudo apt-get install python3-pip gtk+3.0 python3-gi python3-gi-cairo
    sudo pip3 install delicolour

**Fedora 20 and up**:

    sudo yum install python3-pip gtk3 python3-gobject
    sudo pip3 install delicolour

**Arch Linux**:

    sudo install python-pip gtk3 python-gobject
    sudo pip install delicolour

Or, using Yaourt:

    yaourt -S delicolour


## Using

Launch delicolour:

    delicolour

See `delicolour --help` for a list of command-line options.


### Interface

#### Window title

    delicolour: #bba6de [#184c99]

The window title indicates the two current colours, the one being
currently edited surrounded by `[` and `]`.


#### Favorite colours

![](http://ss.0x3b.org/impercipience71.png)

Favorite colours are little squares at the top of the window which
can be set to the current colour by right-clicking them.

The current colour can be set to a favorite colour by left-clicking it.

The `-f`/`--fav-colours-count` and `-F`/`--fav-colours-rows-count`
command-line options control the number of favorite colours.


#### Big rectangle

![](http://ss.0x3b.org/poikilothermal774.png)

The big rectangle at the top shows the two current colours.

A little dot located at the top-left or top-right corner of the
big rectangle indicates which of the two colours is the one currently
being edited. You may switch to one or the other by clicking the
left or right side of the big rectangle.

You can set the initial left and right colours when launching
delicolour with the `-l`/`--left-colour` and `-r`/`--right-colour`
command-line options.


#### Fine-tuning controls

![](http://ss.0x3b.org/unuprightly55.png)

Fine-tuning controls allow to modify the current colour using
buttons to increment/decrement parameters.

The control on the left side is the _increment value_. Pressing one of
the buttons on the right side adds it to or substracts it from the
current values of specific parameters.

The parameters (buttons), from left to right, are:

  * Decrease saturation (_S_ in HSV)
  * Increase saturation
  * Decrease lightness (_L_ in HSL)
  * Increase lightness

The increment value also controls the amount of
incrementation/decrementation of the sliders when scrolling on them
with the mouse wheel.

The `-i`/`--increment` command-line option controls the initial
fine-tuning increment value.


#### RGB

![](http://ss.0x3b.org/stockjobbery593.png)

The RGB sliders control the amount of red, green, and blue in the
current colour.

You can scroll on the sliders and text boxes with the mouse wheel.


#### HSV

![](http://ss.0x3b.org/fuzees835.png)

The HSV sliders control the hue, saturation, and value or the current
colour.

You can scroll on the sliders and text boxes with the mouse wheel. The
hue slider wraps when scrolling on its text box.


#### CSS hex

![](http://ss.0x3b.org/overglide667.png)

The CSS hex text box shows and controls the CSS hexadecimal value of
the current colour.

The CSS hex value can be copied to clipboard by clicking on the text
box and pressing Ctrl+C (no need to select the whole text). If the
_Copy #_ option is checked, a `#` character will be prepended to the
copied value.

You can paste a CSS hex value, with or without a `#` prefix, by
clicking on the text box and pressing Ctrl+V (no need to select the
whole text).

If the `Lowercase` option is checked, the CSS hex value is written in
lowercase when updated.


#### CSS RGB

![](http://ss.0x3b.org/nuzzer45.png)

The CSS RGB text box shows and controls the CSS RGB value of the
current colour.

The CSS RGB value can be copied to the clipboard by clicking on the
text box and pressing Ctrl+C (no need to select the whole text).

You can paste a CSS RGB value, with or without a `#` prefix, by
clicking on the text box and pressing Ctrl+V (no need to select the
whole text).


### Keyboard shortcuts

#### Global shortcuts

The following keyboard shortcuts can be used anytime:

Key | Action
--- | -------
`z` | Set current colour to black
`x` | Set current colour to white
`q` | Decrease saturation
`w` | Increase saturation
`-` | Decrease lightness
`=`/`+` | Increase lightness
`#` | Toggle current colour


#### RGB shortcuts

When the focus is on one of the R, G, and B text boxes, the following
keyboard shortcuts can be used:

Key | Action
--- | -------
`r` | Copy current component value to R text box
`g` | Copy current component value to G text box
`b` | Copy current component value to B text box
