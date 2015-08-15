# delicolour

**_delicolour_** is a lightweight _colour finder_. It uses Gtk+ 3.
It has only been tested on Linux.

![delicolour screenshot](http://ss.0x3b.org/seminaristic317.png)

The goal of delicolour is to have a straightforward interface for
choosing a colour (mainly for Web design), not as advanced as
[Gpick](http://www.gpick.org/), yet still useful and very fluid. The
core principle is: no tabs or other windows, everything accessible
from the main window.


## Notable features

  * Instant updates (moving one slider or modifying one field updates
    the other controls)
  * Big colour rectangle showing your current choice
  * RGB values (0 to 255)
  * HSV values (0 to 359 for hue and 0 to 100 for saturation and value)
  * Scrollable sliders and entries (hue wraps)
  * Fine colour adjustment buttons (increase/decrease saturation and
    lightness) with adjustable increment value
  * CSS hex and RGB strings
  * Intelligent copy/paste (paste `#rrggbb` or `rrggbb` into the hex
    text box and decide if you want to prepend the `#` character when
    copying)


## Installing

In order to install delicolour, the following packages must be installed
on your system:

  * Python 3
  * [PyGObject](https://wiki.gnome.org/action/show/Projects/PyGObject) 3
  * pip for Python 3

The following instructions show how to do so on a few major
distributions:

**Ubuntu**:

    sudo apt-get install python3-pip python3-gi python3-gi-cairo
    sudo pip3 install delicolour

**Debian**:

    sudo apt-get install python3-pip python3-gi python3-gi-cairo
    sudo pip3 install delicolour

**Fedora 20 and up**:

    sudo yum install python3-pip python3-gobject
    sudo pip3 install delicolour

**Arch Linux**:

    sudo install python-pip python-gobject
    sudo pip install delicolour


## Using

Launch delicolour:

    delicolour


### Interface

#### Big rectangle

![](http://ss.0x3b.org/goustie723.png)

The big rectangle at the top shows the current selected colour.


#### Fine-tuning controls

![](http://ss.0x3b.org/nonarsenic673.png)

Fine-tuning controls allow to modify the current colour using
buttons to increment/decrement parameters.

The text box on the left side is the increment value. Pressing one of
the buttons on the right side will add it to or substract it from the
current values of specific parameters.

The parameters (buttons), from left to right, are:

  * Decrease saturation (_S_ in HSV)
  * Increase saturation
  * Decrease lightness (_L_ in HSL)
  * Increase lightness


#### RGB

![](http://ss.0x3b.org/dentinasal310.png)

The RGB sliders control the amount of red, green, and blue in the
current colour.


#### HSV

![](http://ss.0x3b.org/prodigality831.png)

The HSV sliders control the hue, saturation, and value or the current
colour.


#### CSS hex

![](http://ss.0x3b.org/morningtide885.png)

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

![](http://ss.0x3b.org/idealising239.png)

The CSS RGB text box shows and controls the CSS RGB value of the
current colour.

The CSS RGB value can be copied to the clipboard by clicking on the
text box and pressing Ctrl+C (no need to select the whole text).

You can paste a CSS RGB value, with or without a `#` prefix, by
clicking on the text box and pressing Ctrl+V (no need to select the
whole text).


### Keyboard shortcuts

Key | Action
--- | -------
`z` | Set current colour to black
`x` | Set current colour to white
`q` | Decrease saturation
`w` | Increase saturation
`-` | Decrease lightness
`=`/`+` | Increase lightness
