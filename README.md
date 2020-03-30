# hue-tui [![](https://img.shields.io/badge/Version-0.1-green.svg)](https://pypi.org/project/huetui/) ![](https://img.shields.io/badge/License-MIT-orange.svg) 
> A tui for Philips Hue

![Screenshot](https://github.com/channel-42/hue-tui/blob/master/.resources/screen.jpg "A pretty screenshot")

## About 

**hue-tui** is a tui *(Terminal User Interface)* that allows for easy control of your Philips Hue lights. It uses my Hue-API library [hue-snek](https://github.com/channel-42/hue-snek) to communicate with the bridge.

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

## Setup process

To be able to use hue-tui, you need to have your bridge's IP address and a API username. The IP address can be found by e.g. going into your routers network tab and looking for a device with hostname "Philips-hue". To get an API username, check out [this](https://developers.meethue.com/develop/get-started-2/) short guide on the official Hue-Developers site.

Once you have the IP address and unsername, you can start hue-tui by typin `huetui` into a terminal. This should open the first-time-setup, where you can input your IP and username. 

<img align="left" width=47% padding="4" border="20" src="https://github.com/channel-42/hue-tui/blob/master/.resources/setup1.png">    

<img align="right" width=47% padding="4" border="20" src="https://github.com/channel-42/hue-tui/blob/master/.resources/setup2.png">    

<br><br><br> 
       
> Tip: pasting with e.g. CTRL-SHIFT-V works (check what the pasting binding is in your specific terminal emulator) 

To input your IP, navigate the cursor to the IP textfield (it should be there by default) and press ENTER. Then type or paste your bridge's IP address **without http://** at the begining. 

> E.g.: 192.168.178.20

Exit out of the textfield by pressing ESC and move your cursor to the username field. Enter your username just like before and then move your cursor to the big "make login" button. Press ENTER and a popup showing your IP and username should appear. Press ENTER to dismiss the popup and restart huetui by exiting out of the programm (press q).    

After re-opening hue-tui you should see all your lights, groups, scenes, etc. like in the screenshot at the top.

## Using hue-tui

![](https://github.com/channel-42/hue-tui/blob/master/.resources/huetui.gif)

Using hue-tui is easy:   

To **navigate** the different modules use your arrow keys. You'll see your cursor move to the bottom right of the modules, which shows you which module is selected.    
**Enter a module** by pressing ENTER. The selected option will be in bold. Use your arrow keys to navigate inside the module.    
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

## Notes

hue-tui was made using [py_cui](https://github.com/jwlodek/py_cui). Check the project out!
