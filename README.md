# hue-tui ![](https://img.shields.io/badge/Version-0.1-green.svg)(https://badge.fury.io/py/py-cui) ![](https://img.shields.io/badge/License-MIT-orange.svg) 
> A tui for Philips Hue

![Screenshot](https://github.com/channel-42/hue-tui/blob/master/.resources/screen.jpg "A pretty screenshot")

## About 

**hue-tui** is a tui *(Terminal User Interface)* that allows for easy control of your Philips Hue lights. It uses my Hue-API library ![hue-snek](https://github.com/channel-42/hue-snek) to communicate with the bridge.

## Installation

Install hue-tui with:   

`pip install huetui`

This should fetch all the necesary dependencies. Nevertheless, make sure that all dependencies are installed.

Launch hui-tui by typing `huetui` into your terminal.   

Should you get the error `command not found: huetui`, restart your terminal. Should the error persist, check that `$HOME/.local/bin` is in your `$PATH`. This can be done by adding `export PATH="$HOME/.local/bin:$PATH"` to your .bashrc/.zshrc.

### Dependencies
- python3
- hue-snek  (`pip install hue-snek-channel42`)
- py_cui    (`pip install py-cui`)

## Using hue-tui

Using hue-tui is easy:   

To **navigate** the different modules use your arrow keys. You'll see your cursor move to the bottom right of the modules, which shows you which module is selected.    
**Enter a module** by pressing enter. The selected option will be in bold. Use your arrow keys to navigate inside the module.    
Once inside a module, press enter to **execute an action** (e.g. toggle a light).  
To **exit a module** press ESC.
To **quit the programm** simply press q while in the main overview (i.e. not inside a module).

## Progress

**Done**:
- toggle individual lights
- toggle individual groups
- enable a scene for a group
- display bridge information
- ASCII banner
- indicate active lights, groups, scenes
- create automated setup process for bridge information (inital setup function)
- simplify installation process

**TODO**:
- add vim key-bindings for navigating the UI
