#!/bin/python3

import sys
sys.path.append('/path')
from hue_snek import hue, Light
import py_cui as cui

h = hue('http://ip', 'username')

#connection check
if int(h.checkup()) == 1:
    print("Error while connecting to the Hue API")
    sys.exit(0)


class HueTui:
    def __init__(self, master):
        self.master = master
        self.scene = None
        self.bridge = []  #bridge info array

        #add banner
        self.master.add_block_label(str(self.get_logo_text()), 0, 0)

        #items for each menu
        self.lights = h.get_lights("name").values()
        self.groups = h.get_groups("name").values()
        self.scenes = h.get_scenes("name").values()

        #add items to bridge array (dict -> array)
        for param, val in h.get_bridge_info().items():
            self.bridge.append(f"{param}: {val}")

        #creating each menu
        self.lights_menu = self.master.add_scroll_menu("Lights", 1, 0, 2, 1)
        self.groups_menu = self.master.add_scroll_menu("Groups", 3, 0, 2, 1)
        self.scenes_menu = self.master.add_scroll_menu("Scenes", 1, 1, 4, 2)
        self.bridge_information = self.master.add_scroll_menu(
            "Hue Bridge", 0, 1, 1, 2)

        #adding items to each menu
        self.lights_menu.add_item_list(self.lights)
        self.groups_menu.add_item_list(self.groups)
        self.scenes_menu.add_item_list(self.scenes)
        self.bridge_information.add_item_list(self.bridge)

        #adding keycommands
        self.lights_menu.add_key_command(cui.keys.KEY_ENTER, self.toggle_light)
        self.groups_menu.add_key_command(cui.keys.KEY_ENTER, self.toggle_group)
        self.scenes_menu.add_key_command(cui.keys.KEY_ENTER,
                                         command=self.scene_popup)

    def toggle_light(self):
        #toggle a light
        states = h.get_lights()
        for light in states.items():
            if str(self.lights_menu.get()) == str(light[1].name):
                if light[1].state == True:
                    h.set_light(light[0], "on", "false")
                else:
                    h.set_light(light[0], "on", "true")

    def toggle_group(self):
        #toggle a group
        states = h.get_groups()
        for group in states.items():
            if str(self.groups_menu.get()) == str(group[1]["name"]):
                if group[1]["action"]["on"] == True:
                    h.set_group(group[0], "on", "false")
                else:
                    h.set_group(group[0], "on", "true")

    def scene_popup(self):
        #main scene menu with popup to select which group is affected
        groups = list(h.get_groups("name").values())

        self.scene = str(self.scenes_menu.get())

        self.master.show_menu_popup(
            "Select to which group the scene should be applied", groups,
            self.enable_scene)

    def enable_scene(self, inp):
        #enable scene
        group = str(inp)
        groups = h.get_groups("name")

        if group in groups.values():
            group_id = list(groups.keys())[list(groups.values()).index(group)]

            h.set_scene(group_id, self.scene)

    def get_logo_text(self):
        #make banner

        logo = '██╗  ██╗██╗   ██╗███████╗              ████████╗██╗   ██╗██╗\n'
        logo = logo + '██║  ██║██║   ██║██╔════╝              ╚══██╔══╝██║   ██║██║\n'
        logo = logo + '███████║██║   ██║█████╗      █████╗       ██║   ██║   ██║██║\n'
        logo = logo + '██╔══██║██║   ██║██╔══╝      ╚════╝       ██║   ██║   ██║██║\n'
        logo = logo + '██║  ██║╚██████╔╝███████╗                 ██║   ╚██████╔╝██║\n'
        logo = logo + '╚═╝  ╚═╝ ╚═════╝ ╚══════╝                 ╚═╝    ╚═════╝ ╚═╝\n'

        return logo


root = cui.PyCUI(5, 5)
root.set_title("Hue TUI")
Main = HueTui(root)
root.start()
