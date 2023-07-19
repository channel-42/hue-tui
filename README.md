# huetui [![](https://img.shields.io/badge/version-2.0-green.svg)](https://pypi.org/project/huetui/) [![Downloads](https://pepy.tech/badge/huetui)](https://pepy.tech/project/huetui) ![](https://img.shields.io/badge/license-MIT-orange.svg) 
<p align="center"><i>a tui for Philips Hue</i></p>
<p align="center"><img src="https://github.com/channel-42/hue-tui/blob/master/.resources/screen.png" align="center" alt="A pretty screenshot">
</p>

## About 

**huetui** is a **t**erminal **u**ser **i**nterface that allows for easy control of your Philips Hue lights. It uses the official [Hue-Bridge-API](https://developers.meethue.com/) to communicate with the lights and [py_cui](https://github.com/jwlodek/py_cui) for the front-end.

## Installation


### AUR
An [AUR package](https://aur.archlinux.org/packages/huetui) is available for installation via an AUR helper:
```bash
paru -Syy huetui
```

### pip
Install huetui with:
```bash
pip install huetui
```

This should fetch all the necessary dependencies. Nevertheless, make sure that all dependencies are installed.

Launch huetui by typing `huetui` into your terminal.

> Should you get the error `command not found: huetui`, try restarting your terminal. Also, in case your upgrading from v1.0 to v2.0, please make sure to remove the old version before upgrading, as described below.

### Important notice for upgrading from v1.0 to v2.0
Should you have a previous version of huetui installed, **please remove it from your system before upgrading**, either by running

```bash
pip uninstall huetui
```

or deleting the script manually

```bash
cd ~ && rm .local/bin/huetui
```

### Dependencies
These dependencies are needed for installing and running huetui.

- python3
- pip

The following dependencies are downloaded automatically when installing via pip. If you're cloning the repo, make sure to install them manually.
- py_cui
- colorthief
```bash
pip -U install py-cui colorthief
```

## Setup process

**huetui** needs to be provided the *bridge's IP* and an authorized *API user*. 

1. Determine the bridge's IP, e.g. by opening your router's network tab and looking for a device with "Phillips-hue" as its hostname.

2. Obtain an API user by following the [official guide](https://developers.meethue.com/develop/get-started-2/). 

3. Run `huetui` and input the information.


## Using huetui
The status bar will show helpful information about navigation and keybindings.

- **Navigation** is done using the arrow keys. You'll see a cursor move to the bottom right of the modules.
- **Selecting** modules or items is done by pressing ENTER. The selected option will highlighted.
- **Light/group operations**. Move to the desired light or group and:
  + toggle on/off: *ENTER*
  + decrease brightness: *j* 
  + increase brightness: *k* 
  + change color: *c*
- To **exit a module** press ESC.
- To **quit the program** simply press q while in the main overview (i.e. not inside a module).

### Extra features
- To **set wallpaper colors** press *w* while in the main overview.

## Configuring huetui
The colors as well as other settings can be changed in huetui's config file `~/.config/huetui/config.py`. Here are all the available settings:
```python 
# sample config. Edit to your liking.
import py_cui.colors as colors
from huetui.backend.utils import Config
c = Config()
c.ip = "192.168.178.75"
c.api_user = "O4qAaBl9LaXonrNlAu0Pzei3ianWAJuUzYuZpC2I"
c.tui_settings = {
	"unicode": True,
	"wallpaper": "~/Path/To/Wallpaper.jpg",
	"uicolors": {
		"main_ui": colors.WHITE_ON_BLACK,
		"selected": colors.CYAN_ON_BLACK,
		"border": colors.MAGENTA_ON_BLACK,
		"logo": colors.CYAN_ON_BLACK,
		"status_bar": colors.BLACK_ON_MAGENTA,
		"title_bar": colors.BLACK_ON_MAGENTA,
	},
}

```
