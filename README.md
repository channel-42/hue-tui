# huetui [![](https://img.shields.io/badge/version-1.0-green.svg)](https://pypi.org/project/huetui/) [![Downloads](https://pepy.tech/badge/huetui)](https://pepy.tech/project/huetui) ![](https://img.shields.io/badge/license-MIT-orange.svg) 
*a tui for Philips Hue*

![Screenshot](https://github.com/channel-42/hue-tui/blob/master/.resources/screen.jpg "A pretty screenshot")

## About 

**huetui** is a **t**erminal **u**ser **i**nterface that allows for easy control of your Philips Hue lights. It uses my Hue-API library [hue-snek](https://github.com/channel-42/hue-snek) to communicate with the bridge and [py_cui](https://github.com/jwlodek/py_cui) for the front-end.

## Installation

Install huetui with:   

`pip install huetui`

This should fetch all the necesary dependencies. Nevertheless, make sure that all dependencies are installed.

Launch huetui by typing `huetui` into your terminal.   

> Should you get the error `command not found: huetui`, restart your terminal. Should the error persist, check that `$HOME/.local/bin` is in your `$PATH`. This can be done by adding `export PATH="$HOME/.local/bin:$PATH"` to your .bashrc/.zshrc.

### Dependencies
These dependencies are need for installing and running huetui.

- python3
- pip

The following dependencies are downloaded automatically when installing via pip. If you're cloning the repo, make sure to install them manually.
- hue-snek
- py_cui
- Pillow
- colormath
- colorthief
```bash
pip -U install hue-snek-channel42 py-cui Pillow colormath colorthief
```

## Setup process

To be able to use huetui, you need to have your bridge's IP address and a API user. The IP address can be found by going into your routers network tab and looking for a device with "Philips-hue" as it's hostname. To get an API user, check out [this](https://developers.meethue.com/develop/get-started-2/) short guide on the official Hue-Developer site.

Once you have the IP address and api-user, start the tui with `huetui`. huetui will generate a sample config in `~/.config/huetui` and prompt you to run the command again. Then, the first-time-setup will prompt you to enter the bridge's IP and your api-user. 

![setup](https://github.com/channel-42/hue-tui/blob/master/.resources/setup1.png "entering information")
To input your information, navigate the cursor to textfields using the arrow keys and press ENTER. Type or paste in the user info (i.e. IP or api-user) and exit the textfield using ESC. 
> Tip: pasting with e.g. CTRL-SHIFT-V works (check what the pasting binding is in your specific terminal emulator)
> The statusbar at the bottom will show a help text

![setup complete](https://github.com/channel-42/hue-tui/blob/master/.resources/setup2.png "setup complete")


After entering your information, press ENTER on the "Make Login" button and a popup showing your IP and username should appear. Press ENTER to dismiss the popup and restart huetui (press q to exit).    

After re-opening huetui you should see all your lights, groups, scenes, etc. like in the screenshot at the top of the readme.

## Using huetui

![](https://github.com/channel-42/hue-tui/blob/master/.resources/huetui.gif)

### Using huetui is easy:   

- To **navigate** the different modules use your arrow keys. You'll see your cursor move to the bottom right of the modules, which shows you which module is selected.\
- **Enter a module** by pressing ENTER. The selected option will be in bold.\
- Once inside a module, Use your arrow keys to **navigate** and press enter to **execute an action** (e.g. toggle a light).\
- To **change individual light or group brightness** move to the desired light or group and press j (increase) or k (decrease).\
- To **exit a module** press ESC.\
- To **quit the programm** simply press q while in the main overview (i.e. not inside a module).
> The statusbar will show helpful information about navigation and keybindings
### Extra features
- To **start disco mode** navigate and enter the lights menu and press d.
- To **set xrdb colors** navigate to the button and press enter.
- To **set wallpaper colors** navigate to the button and press enter.

## Configuring huetui
The colors as well as other settings can be changed in huetui's config file `~/.config/hue-tui/config.py`. Here are all available settings:
```python 
"""
WPP: string with path to wallpaper picture (png, jpg, etc.)
if set to None, huetui will look for a wallpaper in .fehbg
"""
WPP = None
"""
UNICODE: True or False
Some terminals may have trouble displaying unicode borders
setting UNICODE to false wil disable all unicode
"""
UNICODE = True
"""
SETP_SIZE = int
This is the step size when incrementing the brightness
"""
STEP_SIZE = 30
"""
COLORS: py_cui color
These are the UI colors
"""
COLOR = py_cui.WHITE_ON_BLACK
SELECTED_COLOR = py_cui.CYAN_ON_BLACK
BORDER_COLOR = py_cui.BLUE_ON_BLACK
LOGO_COLOR = py_cui.CYAN_ON_BLACK
STATUSBAR_COLOR = py_cui.BLACK_ON_WHITE
TITLEBAR_COLOR = py_cui.BLACK_ON_WHITE
"""
COLOR_DICT = dict with colors
These colors are used for the preset colors when changing color
by pressing 'c' on a light or group.
Only change the hex values and not the names of the colors!
"""
COLOR_DICT = {
   "red": "#DE3838",
   "blue": "#2122E2",
   "green": "#2EF615",
   "purple": "#5c0099",
   "teal": "#26F0C9"
}
```
## Notes

huetui was made using [py_cui](https://github.com/jwlodek/py_cui), a great ncurses tui-creation library.
