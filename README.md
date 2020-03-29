# hue-tui ![](https://img.shields.io/badge/Status-WIP-red.svg) ![](https://img.shields.io/badge/License-MIT-orange.svg) 
> A tui for Philips Hue

![Screenshot](https://github.com/channel-42/hue-tui/blob/master/.resources/screen.jpg "A pretty screenshot")

## About 

**hue-tui** is a tui *(Terminal User Interface)* that allows for easy control of your Philips Hue lights. It uses my Hue-API library ![hue-snek](https://github.com/channel-42/hue-snek) to communicate with the bridge.

## Setup

> I'm currently working on simplifying the installation process for both hue-tui and hue-snek. The first step is to make hue-snek installable via pip. This will remove the need for a user specific path in the import section.

Since this tui is in it's early development stages, setup is somewhat cumbersome.

After cloning both this and the ![hue-snek](https://github.com/channel-42/hue-snek) repo, add the path of hue_snek.py to hue_tui.py:

```python
#in the import section change /path to your path to hue_snek.py

sys.path.append('/path')    #edit this line
from hue_snek import Hue, Light
```

To start hue-tui it is recommended to setup an alias in your `.zshrc` or `.bashrc` to avoid having to type `python 3 /path/to/hue_tui.py`.

## Usage

Using hue-tui is easy:   

<div style="text-align: justify">
To navigate the different modules use your arrow keys. You'll see your cursor move to the bottom right of the modules, which shows you which module is selected. Enter a module by pressing enter. The selected option will be in bold. To execute an action (e.g. toggle a light) press enter again, and then ESC to exit the module once you're done. To quit the programm, simply press q while in the main overview (i.e. not inside a module).
</div>

## Progress

**Done**:
- toggle individual lights
- toggle individual groups
- enable a scene for a group
- display bridge information
- ASCII banner
- indicate active lights, groups, scenes
- create automated setup process for bridge information (inital setup function)

**TODO**:
- make the installation-process easier

